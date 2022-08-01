# Install Dokku Server

Described in this article: <https://dokku.com/docs/getting-started/advanced-installation/> which points to system specific installation.

## Cloud Ubuntu

```bash
wget https://raw.githubusercontent.com/dokku/dokku/master/bootstrap.sh
sudo DOKKU_BRANCH=master bash bootstrap.sh
```

## Baremetal Ubuntu + Vagrant

```bash
# install dependencies
sudo apt update
sudo apt install git vagrant virtualbox
# virtualbox patch
sudo mkdir -p /etc/vbox
sudo tee networks.conf <<< "* 0.0.0.0/0 ::/0"

git clone https://github.com/dokku/dokku.git
cd dokku

# provision dokku with vagrant
env \
  BOX_CPUS=4 \
  BOX_MEMORY=16384 \
  DOKKU_IP=10.0.0.2 \
  DOKKU_DOMAIN=dokku.maayanlab.cloud \
  FORWARDED_PORT=8080 \
  vagrant up

# login to dokku
vagrant ssh
```

## Baremetal Ingress

In a cloud environment and on a dedicated system, this part is not necessary, but on a system which serves other things an ingress is essential. The simplest way to setup an ingress to serve this and other things is with traefik in a docker-compose. This lets us expose multiple http services on the one port differentiated by the hostname, and can be used for ssh over tls if that is necessary.

- `docker-compose.yml`
  ```yml
  version: '3'
  services:
    ingress:
      image: traefik
      ports:
        - 80:80
        - 443:443
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock
        - ./ingress/traefik.yaml:/etc/traefik/traefik.yaml
        - ./ingress/config:/config
        - ./ingress/data:/data
  ```
- `ingress/traefik.yaml`
  ```yaml
  providers:
    file:
      directory: /config
      watch: true
    docker:
      exposedByDefault: false
  entryPoints:
    web:
      address: :80
    websecure:
      address: :443
  ```
- `ingress/config/dokku-passthrough.yaml`
  ```yaml
  http:
    routers:
      # forward http packets over to the dokku container to be handled
      dokku-http:
        rule: Host(`dokku.maayanlab.cloud`) || Host(`*.dokku.maayanlab.cloud`)
        service: dokku-http
    services:
      dokku-http:
        loadBalancer:
          servers:
          # this is the DOKKU_IP specified in the vagrant install
          - url: "http://10.0.0.2/"
  tcp:
    routers:
      # we'll let dokku handle tls
      dokku-https:
        rule: HostSNI(`dokku.maayanlab.cloud`) || HostSNI(`*.dokku.maayanlab.cloud`)
        service: dokku-https
        tls:
          passthrough: true
      # only necessary if doing ssh-over-tls -- do tls termination to the ssh port
      dokku-ssh:
        rule: HostSNI(`ssh.dokku.maayanlab.cloud`)
        service: dokku-ssh
        tls: {}
    services:
      dokku-https:
        loadBalancer:
          servers:
          # this is the DOKKU_IP specified in the vagrant install
          - address: 10.0.0.2:443
      # only necessary if doing ssh-over-tls
      dokku-ssh:
        loadBalancer:
          servers:
          # this is the DOKKU_IP specified in the vagrant install
          - address: 10.0.0.2:22

  ```
## Configure Dokku

```bash
# setup domain name
dokku domains:set-global dokku.maayanlab.cloud

# use main instead of master
dokku git:set --global deploy-branch main

# setup letsencrypt
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku config:set --global DOKKU_LETSENCRYPT_EMAIL=your_email@gmail.com
dokku letsencrypt:cron-job --add
```
