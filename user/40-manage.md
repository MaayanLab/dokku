# Manage Dokku Deployments

The following Dokku docs should prove helpful for managing dokku deployments:

- [application-management](https://dokku.com/docs/deployment/application-management/)
- [logs](https://dokku.com/docs/deployment/logs/)
- [entering-containers](https://dokku.com/docs/processes/entering-containers/)
- [process-management](https://dokku.com/docs/processes/process-management/)

## Logging

```bash
# help for dokku logs command
dokku logs --help

# show logs for an app
dokku logs my-app
```

## Process management

```bash
# restart an app
dokku ps:restart my-app

# stop an app
dokku ps:stop my-app

# start an app that was stopped
dokku ps:start my-app
```

## Manual container inspection

```bash
# open a shell in your running app in production for debugging
dokku enter my-app
```

## Renaming an app

```bash
dokku apps:rename my-app-oldname my-app-newname
```

## Removing an app

```bash
dokku apps:destroy my-app
```
