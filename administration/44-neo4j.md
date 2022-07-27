# Neo4J (GraphDB)

We repurposed the dokku postgres plugin for neo4j [here](https://github.com/maayanlab/dokku-neo4j), the README has additional documentation. It can be used to launch & manage databases and link them to apps.

Information on how to use this after the fact is in the [user guide](../user/54-neo4j.md).

## Plugin system dependencies

```bash
sudo apt update
sudo apt install net-tools
```

## Plugin installation

```bash
sudo dokku plugin:install https://github.com/maayanlab/dokku-neo4j.git
```

## Neo4j Web UI Proxy

The same kind of trick with the minio-console proxy can be used to make neo4j web ui proxies. But we can grab the hostname out of the `NEO4J_URL` and use port 7474. This way you can intuitively `neo4j:link` the neo4j service to the web ui proxy.

### Source code

The following source code is available as an archive at {downloads}`dokku-neo4j-proxy.tar.gz` for installation convenience.

- `neo4j-proxy/Dockerfile`
  ```Dockerfile
  FROM nginx:alpine

  # add deps
  RUN apk add --no-cache bash gawk

  # add our overrides, the proxy template and the derived environment variable
  ADD default.conf.template /etc/nginx/templates/default.conf.template
  ADD ./entrypoint.sh /entrypoint.sh
  RUN chmod +x /entrypoint.sh

  ENV NGINX_PORT 5000
  ENV NEO4J_URL=""
  # NGINX_UPSTREAM is derived from NEO4J_URL
  ENV NGINX_UPSTREAM ""
  ENV NGINX_CLIENT_MAX_BODY_SIZE 5G

  EXPOSE 5000

  ENTRYPOINT [ "/entrypoint.sh", "/docker-entrypoint.sh" ]
  CMD [ "nginx", "-g", "daemon off;" ]
  ```
- `neo4j/entrypoint.sh`
  ```bash
  #!/bin/bash
  # we extract the ...@(hostname):1234 part of NEO4J_URL and make NGINX_UPSTREAM=hostname:
  NGINX_UPSTREAM_HOSTNAME=$(gawk '{ match($0, /@([^@:]+?):[0-9]+$/, m); print m[1] }' <<< "$NEO4J_URL")
  NGINX_UPSTREAM_PORT="${NGINX_UPSTREAM_PORT:-7474}"
  export NGINX_UPSTREAM="${NGINX_UPSTREAM_HOSTNAME}:${NGINX_UPSTREAM_PORT}"
  "$@"
  ```
- `neo4j/default.conf.template`
  ```template
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

### Dokku install

`my-ui-app` should be replaced with your app name, it will be the public-facing neo4j UI which will be accessed at `my-ui-app.dokku.maayanlab.cloud`. `my-neo4j-db` is the neo4j database created previously.

```bash
dokku apps:create my-ui-app
dokku neo4j:link my-neo4j-db my-ui-app
dokku git:from-image my-ui-app https://dokku.maayanlab.cloud/downloads/dokku-neo4j-proxy.tar.gz
dokku proxy:clear-config my-ui-app
dokku proxy:ports-set my-ui-app 'http:80:80'
dokku letsencrypt:enable my-ui-app
```
