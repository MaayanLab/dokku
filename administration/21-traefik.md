# Traefik Ingress for Dokku

Dokku's default letsencrypt plugin leaves some things to be desired. One alternative would be to use traefik which is rapidly configured and can do letsencrypt ACME/TLS termination for us as well.

We built a plugin: [dokku-traefik](https://github.com/maayanLab/dokku-traefik) with letsEncrypt support specifically using `tlsChallenge` which allows letsencrypt to operate over port 443 only. It automatically registers new deployments by adding traefik configuration to a directory which traefik watches.

In the future this plugin could replace the nginx proxy altogether, but for now it simply deals with TLS termination, forwarding requests to the underyling nginx serving on port 80.

This plugin likely conflicts with dokku-letsencrypt.

## Plugin Installation

```bash
# install the plugin
sudo dokku plugin:install https://github.com/maayanlab/dokku-traefik.git

# activate traefik on port 443
dokku traefik:start
```

## Plugin Usage

Apps can be manually added/removed with `dokku traefik:enable/disable <app>` and traefik's logs can be analysed with `dokku traefik:logs`.
