# Projeto de Métricas para SRE

> Status do Projeto: Em desenvolvimento

## case
### Microsserviço monitorado: Plataforma Datametrics
A empresa DataMetrics possui uma plataforma de dados que serve empresas de diversos setores, para garantir sua qualidade e o respeito de seus clientes ela busca a implementação de indicadores do seu serviço, a partir de agora denominados SLIs e a determinação de objetivos para alcançar em seus serviços, a partir de agora denominados SLOs, para isso precisam que faça um modelo desse monitoramento e com os dados fornecidos veja se os objetivos do último ano foram alcançados e se não foram o que podem fazer para melhora-los.
Os SLIs que devem ser medidos são os seguintes: Frequência de deploys (tabela: esteira_prod); Taxa de Insucesso de Deploy (tabela: esteira_prod); Disponibilidade (tabela: log); Velocidade de resposta a erros (tabela: chamados). No último ano o objetivo foi ter uma frequência de deploy de, no máximo, 3.5 horas , ocorrer, no máximo, 4.5 falhas por deploy, alcançar, no mínimo, 94% de disponibilidade e ter uma velocidade de resposta a erros de, no máximo, 1.5 dias.


## Requisitos
Para rodar esse projeto na sua máquina, é necessário que tenha instalado:
- Docker Desktop
- Ubuntu 20.04.6 LTS (pode ser utilizado por meio do WSL2)
- Cluster Big Data (HDFS, Hive, Spark, MySQL)
- Python 3


## Projeto
Para baixar o Cluster Big Data é necessário, no mínimo, 16 Gb de RAM e executar os seguintes comandos:
```
git clone https://github.com/rodrigo-reboucas/docker-bigdata.git
```

Para instala-lo execute dentro da pasta "docker-bigdata":
```
docker-compose pull
```

Para executar os containers baixados pela primeira vez basta executar:
```
docker-compose up -d
```

O primeiro passo é criar as tabelas que serão utilizadas para montar os indicadores de observabilidade. Para isso criei o arquivo 
