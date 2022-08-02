# MinIO (S3)

[MinIO](https://min.io/) offers open source S3 compatible object storage, thier solution is very advanced and can scale the way AWS native S3 can across many nodes, alternatively it works just as well on a single system with the added benefit of coming with a easy-to-use user interface that can also be used to manage access controls.

MinIO is launchable with docker and can thus be served on dokku, though some tweaks/configuration are necessary.

## MinIO S3 server

MinIO's docker image is good to go, though we can bake in some convenient augmentations including the fixed console-address port, unprivileged user, and data directory.

### Source code

The following source code is available as an archive at {downloads}`dokku-minio-console.tar.gz` for installation convenience.

Create a git repo directory `minio` and add the following file:

- `/minio/Dockerfile`
  ```Dockerfile
  FROM minio/minio:latest
  RUN adduser -u 32769 -m -U dokku
  USER dokku
  RUN mkdir -p /home/dokku/data
  # s3 port
  EXPOSE 9000
  # console port
  EXPOSE 9001
  VOLUME /home/dokku/data
  CMD ["server", "--console-address", ":9001", "/home/dokku/data"]
  ```

### Dokku install

```bash
# create and configure minio
dokku app:create minio
# random user/pass
dokku config:set --no-restart minio MINIO_ACCESS_KEY=$(echo `openssl rand -base64 45` | tr -d \=+ | cut -c 1-20)
dokku config:set --no-restart minio MINIO_SECRET_KEY=$(echo `openssl rand -base64 45` | tr -d \=+ | cut -c 1-32)
# configure
dokku config:set --no-restart minio MINIO_SERVER_URL=https://minio.dokku.maayanlab.cloud
dokku config:set --no-restart minio MINIO_BROWSER_REDIRECT_URL=https://minio-console.dokku.maayanlab.cloud
dokku config:set --no-restart minio MINIO_DOMAIN=minio.dokku.maayanlab.cloud
dokku config:set --no-restart minio CONSOLE_SECURE_TLS_REDIRECT="off"
# push-to-deploy minio to dokku
dokku git:from-archive minio https://dokku.maayanlab.cloud/downloads/dokku-minio.tar.gz
# (or if working from local repo)
#git push -u production
# persistent storage
sudo mkdir -p /var/lib/dokku/data/storage/minio
sudo chown 32769:32769 /var/lib/dokku/data/storage/minio
dokku storage:mount minio /var/lib/dokku/data/storage/minio:/home/dokku/data
# reconfigure port (use port 9000)
dokku proxy:ports-set minio http:80:9000
# ssl termination with dokku-letsencrypt if required (not with traefik)
#dokku letsencrypt:enable minio
# update port mappings -- serve 9000 as minio, and 9001 internally
dokku proxy:ports-set minio https:443:9000 http:9001:9001
# increase client-max-body-size for upload limits
dokku nginx:set minio client-max-body-size 5G
dokku proxy:build-config minio
# review configuration including user/password
dokku config:show minio
```

## MinIO web console proxy

Exposing the minio console (served on port 9001) externally can be done with an app which proxies to it (even though it's served by the `minio` image). nginx can be used for this purpose:

### Source code

The following source code is available as an archive at {downloads}`dokku-minio-console.tar.gz` for installation convenience.

Create a git repo directory `minio-console` and add the following file(s):

- `/minio-console/default.conf.template`
  ```nginx.conf
  server {
    listen ${NGINX_PORT};

    client_max_body_size ${NGINX_CLIENT_MAX_BODY_SIZE};

    location / {
      proxy_pass  http://nginx-upstream;
      http2_push_preload on;
      proxy_http_version 1.1;
      proxy_read_timeout 60s;
      proxy_buffer_size 4096;
      proxy_buffering on;
      proxy_buffers 8 4096;
      proxy_busy_buffers_size 8192;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $http_connection;
      proxy_set_header Host $http_host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $server_port;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header X-Request-Start $msec;
    }
  }

  upstream nginx-upstream {
    server ${NGINX_UPSTREAM};
  }
  ```
- `/minio-console/Dockerfile`
  ```Dockerfile
  FROM nginx
  ADD default.conf.template /etc/nginx/templates/default.conf.template
  ENV NGINX_PORT 5000
  # 172.17.0.1 corresponds to out-of-docker "localhost"
  ENV NGINX_UPSTREAM 172.17.0.1:9001
  ENV NGINX_CLIENT_MAX_BODY_SIZE 5G
  EXPOSE 5000
  ```

### Dokku install

```bash
# configure minio-console app
dokku app:create minio-console
# push-to-deploy minio-console to dokku
dokku git:from-archive minio-console https://dokku.maayanlab.cloud/downloads/dokku-minio-console.tar.gz
# (or if working from local repo)
#git push -u production
# ssl termination with dokku-letsencrypt if required (not with traefik)
#dokku letsencrypt:enable minio-console
# increase client-max-body-size for upload limits
dokku nginx:set minio client-max-body-size 5G
dokku proxy:build-config minio
```
