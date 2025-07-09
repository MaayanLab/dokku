# Manage Applications with Docker Compose

We recommend adopting docker and docker compose for your managing your app in production. Docker has [extensive documentation](https://docs.docker.com/) which you can refer to but here is a basic example.

While docker compose can be use to run containers on your own system, kube compose works the same way but manages containers running remotely on the cluster. Get everything running on your own system first, and things should work when they get deployed to the cluster.

## Example
Make the following additions in your app directory:

- `Dockerfile`: Use this define a container capable of running your app
  ```Dockerfile
  # this base image has python setup and ready to go
  FROM python

  # install dependencies
  COPY requirements.txt /app/requirements.txt
  RUN pip install -r /app/requirements.txt

  # add source to app
  COPY . /app
  WORKDIR /app

  # the port your app uses -- this is essential for dokku deployment
  EXPOSE 5000

  # what to do when the container starts
  CMD gunicorn --bind 0.0.0.0:5000 app:app
  ```
- `docker-compose.yaml`: Manage potentially multiple containers for running your app
  ```yaml
  services:
    # generally good practice to prefix service by your app name, change yourapp to your app's name
    yourapp-app:
      build: .
      image: your-docker-username/yourapp-app:0.1.0
      environment:
      # gets this from your .env
      - YOURAPP_WHAT
      ports:
      # 5000 (your system, i.e. http://localhost:5000) maps to the container's port 5000
      - 5000:5000
      x-kubernetes:
        annotations:
          # this is where it will be deployed when it is published
          maayanlab.cloud/ingress: https://yourapp.k8s.dev.maayanlab.cloud
  x-kubernetes:
    name: yourapp
  ```
- `README.md`
  ```md
  ...

  ## Deploy
  `docker compose build # build the container`
  `docker compose up # verify that it works the way you expect at http://localhost:5000`
  ```

## App management

## Build the container for a service

```bash
docker compose build yourapp-app
```

## Run your app's services

```bash
# -d flag runs them in the background
docker compose up -d
```

## Logging

```bash
# get logs of a service
docker compose logs yourapp-app
```

## Process management

```bash
# restart a service
docker compose restart yourapp-app

# stop a service
docker compose stop yourapp-app

# start a service that was stopped
docker compose start yourapp-app
```

## Manual container inspection

```bash
# open a shell in your running app for debugging
docker compose exec -it yourapp-app /bin/sh
```

## Stopping your app

```bash
docker compose down

# if you have persistent data, you can opt-in to remove them as well
docker compose down -v
```
