# Neo4J

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
