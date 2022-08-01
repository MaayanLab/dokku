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

# Configure Dokku

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
