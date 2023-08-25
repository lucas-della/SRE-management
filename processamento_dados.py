#Importação da biblioteca
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql import functions as F
from pyspark.sql.functions import col, datediff, lag, unix_timestamp, concat, lit, year, weekofyear

#Caminho driver
caminho_driver = "/opt/spark/jars/mysql-connector-java-5.1.47.jar"

#Instanciar o objeto Spark
spark = SparkSession.builder \
        .appName("LerTabelaMySQL") \
        .config("spark.jars", caminho_driver) \
        .config("spark.sql.catalogImplementation", "hive") \
        .config("spark.sql.warehouse.dir", "/user/hive/warehouse/") \
        .enableHiveSupport() \
        .getOrCreate()

#Informações para criar conexão com o MySQL
url = "jdbc:mysql://database/della"
propriedades = {
            "user": "root",
            "password": "secret",
            "driver": "com.mysql.jdbc.Driver"
                    }
#Teste de caminho
print(spark.conf.get("spark.sql.catalogImplementation"))

##BASE DE DADOS DE CHAMADOS

#Informações da tabela para coletar os dados
nome_tabela = "tb_chamados"

chamados = spark.read.jdbc(url=url, table=nome_tabela, properties=propriedades)

#Filtrar a coluna de status com "closed"
chamados = chamados.where(chamados.incident_state == "Closed")

#Criar coluna com a semana do ano em que o chamado foi aberto
ano = year('opened_at')
semana = weekofyear('opened_at')
chamados = chamados.withColumn('week_opened_at', concat(ano, lit("-"), semana))

#Criar coluna com a diferença de tempo entre abertura e fechamento de chamados
chamados = chamados.withColumn('tempo_chamado_horas', (unix_timestamp('closed_at') - unix_timestamp('opened_at')) / (60*60) )

#Salvar a tavela no Hive
chamados.write.saveAsTable("della.tb_chamados", mode="overwrite")

##BASE DE DADOS DE ESTEIRA DE PRODUÇÃO

#Informações da tabela para coletar dados
nome_tabela = "tb_esteira_prod"

esteira_prod = spark.read.jdbc(url=url, table=nome_tabela, properties=propriedades)

#Criar coluna com a semana do ano em que o chamado foi aberto
ano = year('dt_deploy')
semana = weekofyear('dt_deploy')
esteira_prod = esteira_prod.withColumn('week_dt_deploy', concat(ano, lit("-"), semana))

#Criar coluna com a diferença de tempo entre o commit e o deploy
esteira_prod = esteira_prod.withColumn('tempo_deploy_horas', (unix_timestamp('dt_deploy') - unix_timestamp('dt_commit')) / (60*60) )

#Criar coluna com a diferença de tempo entre deploys (Deploy Frequence)
ordenar_eventos = Window.orderBy(col("dt_deploy"))
esteira_prod = esteira_prod.withColumn("data_anterior", lag(col("dt_deploy")).over(ordenar_eventos))
esteira_prod = esteira_prod.withColumn("DF", datediff(col("dt_deploy"), col("data_anterior")))
esteira_prod = esteira_prod.na.fill(0, subset=["DF"])
esteira_prod = esteira_prod.drop("data_anterior")

#Salvar a tavela no Hive
esteira_prod.write.saveAsTable("della.tb_esteira_prod", mode="overwrite")

##BASE DE DADOS DE LOG

#Informações da tabela para coletar dados
nome_tabela = "tb_logs"

log = spark.read.jdbc(url=url, table=nome_tabela, properties=propriedades)

#Criar coluna com a diferença de tempo entre abertura e fechamento de chamados
log = log.withColumn('tempo_erro_horas', (unix_timestamp('timestamp_up') - unix_timestamp('timestamp_down')) / (60*60) )

#Salvar a tavela no Hive
log.write.saveAsTable("della.tb_log", mode="overwrite")

##TABELA QTD CHAMADOS E DEPLOYS POR SEMANA

#Criar duas tabelas relacionando as semanas e a quantidade de chamados e de deploys
contagem_chamados_semanas = chamados.groupBy('week_opened_at').agg(F.count("*").alias("quantidade_chamados"))
contagem_deploys_semanas = esteira_prod.groupBy('week_dt_deploy').agg(F.count("*").alias("quantidade_deploys"))

#Trocar o nome das colunas de semana para serem iguais
contagem_chamados_semanas = contagem_chamados_semanas.withColumnRenamed("week_opened_at", "semana")
contagem_deploys_semanas = contagem_deploys_semanas.withColumnRenamed("week_dt_deploy", "semana")

#Juntar ambas tabelas pela coluna de semanas
contagem_chamados_deploys_semanas = contagem_chamados_semanas.join(contagem_deploys_semanas, on="semana", how="full")

#Salvar a tavela no Hive
contagem_chamados_deploys_semanas.write.saveAsTable("della.tb_semanas", mode="overwrite")

#Encerrar a sessão
spark.stop()
