# Common Deployment Issues and their Solutions

We've created and maintain this list of common deployment issues people experience since errors can sometimes be cryptic.

## "Not a git repository"

Your project needs to be under version control, please review the [setup documentation](./20-setup.md) about git and github. If you've already configured your project with git, you're probably not running the command in the same directory of your project.

## "Unable to select a buildpack"

Your error might look like this:
```
-----> Unable to select a buildpack
remote:  !     Failure during app build
remote: 2024/07/30 14:16:01 exit status 1
```

The issue is likely that you forgot to create a `Dockerfile`, please review the [setup documentation](./20-setup.md).

## "Pull access denied"

Your error might look like this:
```
 => ERROR [internal] load metadata for docker.io/dokku/test:latest                                                                                          0.1s
------
 > [internal] load metadata for docker.io/dokku/test:latest:
------
dokku/test:latest: pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
 !     Failure injecting docker labels on image
```

The actual issue is that you've probably built the image on a different platform. You should add the `--platform linux/amd64` flag to your `docker build` command.

## "Failed to load database 'neo4j'"

Your error might look like this:
```
Failed to load database 'neo4j': Not a valid Neo4j archive: reading from stdin
Load failed for databases: 'neo4j'
Load failed for databases: 'neo4j'
```

The issue is that with neo4j-v5 the database dump to stdout is partially broken. The solution is to run the following.

First run:

```
docker-compose run neo4j-v5 neo4j-admin database dump neo4j
```

On docker desktop then navigate to the most recent container run and navigate to the `Inspect` tab. From there find the entry `Mounts/data` and click on the link button. From there navigate to the `dumps` folder and save the neo4j.dump file. 

We can then now properly load the dump file as we would normally.

```
dokku neo4j:import my-app < ./neo4j.dump
```
