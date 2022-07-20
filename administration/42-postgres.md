# PostgreSQL (RDMS)

Dokku has official support for [dokku-postgres](https://github.com/dokku/dokku-postgres), this plugin is well documented and can be used to launch databases and link them to apps.

Information on how to use this after the fact is in the [user guide](../user/52-postgres.md).

## Plugin system dependencies

```bash
sudo apt update
sudo apt install net-tools
```

## Plugin installation

```bash
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```
