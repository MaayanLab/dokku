# Dockerized Services

Applications should typically be stateless, but naturally applications will inevitably require access to some kind of database or file storage. A number of services can be launched with docker for this purpose, and apps can link to those services.

- [PostgreSQL (RDMS)](./61-postgres.md): a popular relational database we recommend
- [MariaDB (RDMS)](./62-mariadb.md): another popular relational database compatible with mysql
- [Neo4J (GraphDB)](./63-neo4j.md): a graph database we use frequently in the lab
- [MinIO (S3)](./64-minio.md): a cloud file storage service
