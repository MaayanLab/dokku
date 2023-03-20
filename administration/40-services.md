```{warning}
This is for maintainers of the dokku backend -- if you are a regular user of dokku, the information on this page is likely not useful for you, please don't attempt to run the commands stated in this section.
```

# Dokku Services

Applications should typically be stateless, but naturally applications will inevitably require access to some kind of database or file storage. A number of services can be launched on dokku for this purpose, and apps can link to those services.

- [MinIO (S3)](./41-minio.md)
- [PostgreSQL (RDMS)](./42-postgres.md)
- [MariaDB (RDMS)](./43-mariadb.md)
- [Neo4J (GraphDB)](./44-neo4j.md)
