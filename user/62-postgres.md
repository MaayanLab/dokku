# PostgreSQL (RDMS)

[Postgres](https://www.postgresql.org/) is a good and mature open source relational database.

## Adding postgres to your app's docker-compose.yaml

```yaml
services:
  # ...
  yourapp-postgres:
    image: postgres:17
    environment:
    # this should be in your .env file and set to a long random string
    - POSTGRES_PASSWORD
    ports:
    - 5432:5432
    volumes:
    - yourapp-postgres-data:/var/lib/postgresql/data

volumes:
  yourapp-postgres-data:
    x-kubernetes:
      size: 1Gi
      class: local-path
```

## Transfering your local database to the production database

```bash
# stream dump output directly to pg_restore on db runnning in cluster
docker compose exec -t yourapp-postgres pg_dump -Fc --no-acl --no-owner -h localhost -U postgres -w postgres \
  | sshkube run kube-compose exec -i yourapp-postgres pg_restore -Fc -h localhost -U postgres -w postgres -

# you can of course go the other way around as well if you needed to get information from production
sshkube run kube-compose exec -t yourapp-postgres pg_dump -Fc --no-acl --no-owner -h localhost -U postgres -w postgres \
  | docker compose exec -i yourapp-postgres pg_restore -Fc -h localhost -U postgres -w postgres -
```

## Accessing the database in your app

The database will be accessible at the hostname corresponding to your service name, but it's best practice to set up an environment variable to specify the location. For example, in python:

- `.env`:
  ```
  # so you can test accessing the database locally
  DATABASE_URL=postgres://postgres:YOURPOSTGRES_PASSWORD@localhost:5432/postgres
  ```
- `docker-compose.yaml`:
  ```yaml
  services:
    yourapp-app:
      environment:
      # so your app container goes to the right location, **NOT localhost**
      - DATABASE_URL=postgres://postgres:${POSTGRES_PASSWORD}$@yourapp-postgres:5432/postgres
  ```
- `app.py`:
  ```python
  import os
  import psycopg2

  DATABASE_URL = os.environ.get('DATABASE_URL')
  assert DATABASE_URL is not None, 'Missing DATABASE_URL environment variable to connect to the database'

  # connect to db
  conn = psycopg2.connect(DATABASE_URL)

  # ... use conn in your app to build queries ...

  conn.close()
  ```
