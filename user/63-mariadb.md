# MariaDB (RDMS)

[Mariadb](https://mariadb.org/) is a good and mature open source relational database and drop-in replacement for MySQL.

## Adding mariadb to your app's docker-compose.yaml

```yaml
services:
  # ...
  yourapp-mariadb:
    image: mariadb:11
    environment:
    - MARIADB_DATABASE=mariadb
    - MARIADB_USER=mariadb
    # this should be in your .env file and set to a long random string
    - MARIADB_PASSWORD
    ports:
    - 3306:3306
    volumes:
    - yourapp-mariadb-data:/var/lib/mysql

volumes:
  yourapp-mariadb-data:
    x-kubernetes:
      size: 1Gi
      class: local-storage
```

## Transfering your local database to the production database

```bash
# stream dump output directly to pg_restore on db runnning in cluster
docker compose exec -t yourapp-mariadb mariadb-dump mariadb \
  | sshkube run kube-compose exec -i yourapp-mariadb mysql

# you can of course go the other way around as well if you needed to get information from production
sshkube run kube-compose exec -t yourapp-mariadb mariadb-dump mariadb \
  | docker compose exec -i yourapp-mariadb mysql
```

## Accessing the database in your app

The database will be accessible at the hostname corresponding to your service name, but it's best practice to set up an environment variable to specify the location. For example, in python:

- `.env`:
  ```
  # so you can test accessing the database locally
  DATABASE_URL=mariadb://mariadb:YOURMARIADB_PASSWORD@localhost:5432/mariadb
  ```
- `docker-compose.yaml`:
  ```yaml
  services:
    yourapp-app:
      environment:
      # so your app container goes to the right location, **NOT localhost**
      - DATABASE_URL=mariadb://mariadb:${MARIADB_PASSWORD}$@yourapp-mariadb:5432/mariadb
  ```
- `app.py`:
  ```python
  import os
  import mysql.connector

  DATABASE_URL = os.environ.get('DATABASE_URL')
  assert DATABASE_URL is not None, 'Missing DATABASE_URL environment variable to connect to the database'

  # connect to db
  conn = mysql.connector.connect(DATABASE_URL)

  # ... use conn in your app to build queries ...

  conn.close()
  ```
