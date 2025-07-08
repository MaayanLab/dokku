# Neo4J (GraphDB)

[Neo4J](https://neo4j.com/) is an open source and enterprise graph database.

## Adding neo4j to your app's docker-compose.yaml

```yaml
services:
  # ...
  yourapp-neo4j:
    image: neo4j:4.4.8-community
    environment:
    - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
    # this should be in your .env file and set to a long random string
    - NEO4J_PASSWORD
    ports:
    - 7687:7687
    - 7474:7474
    volumes:
    - yourapp-neo4j-data:/data

volumes:
  yourapp-neo4j-data:
    x-kubernetes:
      size: 1Gi
      class: local-storage
```

## Transfering your local database to the production database

```bash
# neo4j must be stopped for dump/load
docker compose stop yourapp-neo4j
sshkube run kube-compose stop yourapp-neo4j

# stream dump output directly to pg_restore on db runnning in cluster
docker compose run -t yourapp-neo4j neo4j-admin database dump neo4j \
  | sshkube run kube-compose run -i yourapp-neo4j neo4j-admin database load neo4j

# you can of course go the other way around as well if you needed to get information from production
sshkube run kube-compose run -t yourapp-neo4j neo4j-admin database dump neo4j \
  | docker compose run -i yourapp-neo4j neo4j-admin database load neo4j

# start them back up when done
docker compose start yourapp-neo4j
sshkube run kube-compose start yourapp-neo4j
```

## Accessing the database in your app

The database will be accessible at the hostname corresponding to your service name, but it's best practice to set up an environment variable to specify the location. For example, in python:

- `.env`:
  ```
  # so you can test accessing the database locally
  NEO4J_URL=bolt://neo4j:YOURNEO4J_PASSWORD@localhost:7687
  ```
- `docker-compose.yaml`:
  ```yaml
  services:
    yourapp-app:
      environment:
      # so your app container goes to the right location, **NOT localhost**
      - NEO4J_URL=bolt://neo4j:${NEO4J_PASSWORD}$@yourapp-neo4j:7687
  ```
- `app.py`:
  ```python
  import os
  from py2neo import Graph

  NEO4J_URL = os.environ.get('NEO4J_URL')
  assert NEO4J_URL is not None, 'Missing NEO4J_URL environment variable to connect to the database'

  # connect to db
  graph = Graph(NEO4J_URL)

  # ... use graph in your app to build queries ...
  ```

## Accessing Neo4J Web Browser

<http://localhost:7474/browser>
