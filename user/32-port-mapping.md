# Dokku Port Mapping

After creating your app, it's possible that either dokku didn't auto-detect the ports properly or the port has changed. In this case, it will be necessary to fallback to manual port mapping.

## Setup terminal

As in the deployment phase, dokku commands can be setup with
```bash
alias dokku="ssh -t dokku@dokku.maayanlab.cloud"
```

## Show existing ports

```bash
dokku proxy:report my-app
```

Example:
```
=====> minio-console proxy information
       Proxy enabled:                 true
       Proxy port map:                http:80:80 https:443:80
       Proxy type:                    nginx
```

The port maps follow the docker standard, `scheme:host-port:container-port` where the `scheme` tells dokku whether secure (https) or insecure traffic (http) should flow. `host port` is the entrypoint into the dokku server, it should be 80 for http or 443 for https. `container port` is the port the container serves on, common examples include 80, 5000, and 8080.

## Setting up port mappings

```bash
# if not enabled, enable the proxy
dokku proxy:enable my-app

# replace 5000 with the port your container is using
dokku proxy:ports-set my-app http:80:5000 https:443:5000

# rebuild the nginx configuration to reflect new port mappings
dokku proxy:build-config my-app
```

If things are still not working you might want to check the nginx config to verify it has your changes
```bash
dokku nginx:show-config my-app
```

The `upstream` at the bottom should be using the container port and the `listen` clauses should show the host ports. If this looks good but it still doesn't work, there is likely an issue with the container, test it locally.
