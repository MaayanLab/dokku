# MariaDB

Dokku has official support for [dokku-mariadb](https://github.com/dokku/dokku-mariadb), this plugin is well documented and can be used to launch databases and link them to apps.

Information on how to use this after the fact is in the [user guide](../user/53-mariadb.md).

## Plugin system dependencies

```bash
sudo apt update
sudo apt install net-tools
```

## Plugin installation

```bash
sudo dokku plugin:install https://github.com/dokku/dokku-mariadb.git
```
