```{warning}
This is for maintainers of the dokku backend -- if you are a regular user of dokku, the information on this page is likely not useful for you, please don't attempt to run the commands stated in this section.
```

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
