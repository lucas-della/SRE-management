# Projeto de Métricas para SRE

> Status do Projeto: Em desenvolvimento

Para rodar esse projeto na sua máquina, é necessário que tenha instalado:
```
Docker Desktop
Ubuntu 20.04.6 LTS (pode ser utilizado por meio do WSL2)
Cluster Big Data
```
Para baixar o Cluster Big Data é necessário, no mínimo, 16 Gb de RAM e executar os seguintes comandos:
```
mkdir treinamentos

cd treinamentos

git clone https://github.com/rodrigo-reboucas/docker-bigdata.git
```

Para instala-lo execute dentro da pasta "docker-bigdata":
```
docker-compose pull

docker image ls #lista as imagens baixadas
```

Para executar os containers baixados basta executar:
```
docker-compose up -d

docker containers ls #lista os comandos em execução
```
