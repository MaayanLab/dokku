```{warning}
This is for maintainers of the dokku backend -- if you are a regular user of dokku, the information on this page is likely not useful for you, please don't attempt to run the commands stated in this section.
```

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

## SSH over HTTPS Passthrough

If port 22 is not easily utilized, ssh can be used over https with an extra step on the user side of things. With the traefik plugin in place, an additional rule can be added. We perform TLS termination with traefik and forward decoded traffic to port 22. On the client side, a `openssl s_client` ProxyCommand can be used to leverage this for ssh.

```bash
sudo -u dokku cat > /var/lib/dokku/services/traefik/config/ssh-passthrough.yaml <<EOF
tcp:
  routers:
    dokku-ssh:
      rule: HostSNI(`ssh.dev.maayanlab.cloud`)
      entryPoints:
        - websecure
      service: dokku-ssh
      tls:
        certResolver: letsencrypt
  services:
    dokku-ssh:
      loadBalancer:
        servers:
          # 172.17.0.1 is "localhost" (the actual system) when in docker
          - address: 172.17.0.1:22
EOF
```

## Root redirect

It's convenient to run the docs on a subdomain, i.e. `dokku.dev.maayanlab.cloud` but it would be good for the root domain to point somewhere. A root redirect from `dev.maayanlab.cloud => dokku.dev.maayanlab.cloud` can be setup as follows:

```bash
sudo -u dokku cat > /var/lib/dokku/services/traefik/config/root-redirect.yaml <<EOF
http:
  routers:
    dev-maayanlab-cloud:
      rule: Host(`dev.maayanlab.cloud`)
      entryPoints:
        - websecure
      middlewares:
        - dev-maayanlab-cloud-redirect
      service: noop@internal
      tls:
        certResolver: letsencrypt
  middlewares:
    dev-maayanlab-cloud-redirect:
      redirectRegex:
        regex: "^http(s?)://dev.maayanlab.cloud/(.*)"
        replacement: "http${1}://dokku.dev.maayanlab.cloud/${2}"
EOF
```
