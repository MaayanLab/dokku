# Install Dokku Server

Described in this article: <https://dokku.com/docs/getting-started/advanced-installation/> which points to system specific installation.

## Cloud Ubuntu

```bash
wget https://raw.githubusercontent.com/dokku/dokku/master/bootstrap.sh
sudo DOKKU_BRANCH=master bash bootstrap.sh
```

## Vagrant

```bash
git clone https://github.com/dokku/dokku.git
cd dokku
DOKKU_DOMAIN=dokku.maayanlab.cloud vagrant up
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
