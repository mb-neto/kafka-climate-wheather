## Execução dos Serviços

Os primeiros servidores inicializados devem ser, em ordem de execução: PostgreSQL, pgAdmin4, Zookeeper e Apache Kafka. Após a constatação que todos os serviços estão rodando normalmente, deve-se subir o servidor do Apache Kafka Connect e, posteriormente, o servidor para Central de Controle. Confere-se abaixo a sequência de comandos de linha para terminal. 

```
$ docker-compose --env-file compose.env up -d postgres-server postgres-admin zookeeper kafka
$ docker-compose --env-file compose.env up -d kafka-connect control-center 
```

Com o servidor do Kafka Connect rodando normalmente, conectado ao Kafka, Zookeeper e Central de Controle, sob a mesma rede do servidor de banco de dados, aplica-se os conectores pg-producer e pg-consumer por meio de comandos curl a API REST do Kafka Connect. 

```
$ curl -i -X POST -H "Accept:application/json" -H "Content-Type:appli cation/json" http://localhost:8083/connectors/ -d @kafka/source.json
$ curl -i -X POST -H "Accept:application/json" -H "Content-Type:appli cation/json" http://localhost:8083/connectors/ -d @kafka/sink.json
```

Posteriormente, emite-se o comando a seguir para construção e inicialização do contêiner referente a aplicação Python que, por sua vez, dispara a primeira coleta e inserção dos dados.

```
$ docker-compose --env-file config/compose.env up -d --build app
```
