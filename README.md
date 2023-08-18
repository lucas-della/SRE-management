# Projeto de Métricas para SRE

> Status do Projeto: Em desenvolvimento

## Motivação
Ao aprender sobre a cultura Dev Ops, estando no dia a dia de uma equipe de SRE, comecei a ter contato com muitos termos como SLI, SLO, SLA e Eror Bugdet e para consolidar os conhecimentos adquiridos montei um projeto para uma plataforma de dados para análise de métricas para SRE. Aproveito também que conclui um curso de Big Data e colocai em prática os conhecimentos adquiridos.

## Case para Desenvolvimento
### Microsserviço monitorado: Plataforma Datametrics
A empresa DataMetrics possui uma plataforma de dados que serve empresas de diversos setores, para garantir sua qualidade e o respeito de seus clientes ela busca a implementação de indicadores do seu serviço, a partir de agora denominados SLIs e a determinação de objetivos para alcançar em seus serviços, a partir de agora denominados SLOs, para isso precisam que faça um modelo desse monitoramento e com os dados fornecidos veja se os objetivos do último ano foram alcançados e, se não foram, o que podem fazer para melhora-los.
Os SLIs que devem ser medidos são os seguintes: Frequência de deploys (tabela: esteira_prod); Taxa de Insucesso de Deploy (tabela: esteira_prod); Disponibilidade (tabela: log); Velocidade de resposta a erros (tabela: chamados). No último ano o objetivo foi ter uma frequência de deploy de, no máximo, 3.5 horas , ocorrer, no máximo, 4.5 falhas por deploy, alcançar, no mínimo, 94% de disponibilidade e ter uma velocidade de resposta a erros de, no máximo, 1.5 dias.


## Requisitos
Para rodar esse projeto na sua máquina, é necessário que tenha instalado:
- Docker Desktop
- Ubuntu 20.04.6 LTS (pode ser utilizado por meio do WSL2)
- Cluster Big Data (HDFS, Hive, Spark, MySQL)
- Python 3


## Projeto
### Instalação do Cluster Big Data
Para baixar o Cluster Big Data basta executar o seguinte comando:
```
git clone https://github.com/rodrigo-reboucas/docker-bigdata.git
```

Para instala-lo execute dentro da pasta "docker-bigdata":
```
docker-compose pull
```

Para iniciar os containers baixados pela primeira vez basta executar:
```
docker-compose up -d
```

### Criação das tabelas
Com o ambiente montado, o primeiro passo que tomei foi criar as tabelas que utilizaria para análise de métricas (que pode ser encontrado no arquivo ProjetoJ.ipynb), é importante ressaltar que os indicadores do case foram escolhidos como os melhores indicadores para o modelo de negócios proposto, não há um certo e errado, mas sim o que atende melhor e mantém o negócio funcional ou não.
Para a criação das tabelas utilizei principalmente a biblioteca Faker do Python e após definir os parâmetros necessários, gerei ela em CSV para poder ingerir no MySQL.

> A biblioteca Faker é extremamente maleável com as suas necessidades, além de possuir alguns geradores de dados nativos, ela permite que crie geradores com diferentes strings e números. O potencial da biblioteca aumenta consideravelmente quando são utilizados estruturas de codificação do Python e a criação de funções.
