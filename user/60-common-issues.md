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
