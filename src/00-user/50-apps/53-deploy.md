# Deploy with Kube-Compose

Here we walk through the basics of pushing your app to the cluster. Your app should be working locally via docker-compose before trying to push it to the cluster.

## Push docker containers
The containers you've built must be published on dockerhub so that they are accessible outside of your own system, this can be done with:
```bash
docker compose push
```

## Publish to kubernetes cluster
`kube-compose` is designed to be analogous with docker compose, so whatever you would have used with docker compose, likely works with kube-compose as well. For example, to launch the app on the cluster use:

```bash
# `sshkube run` ensures that your configured access to the cluster is set up
sshkube run kube-compose up

# you could alternatively setup your shell with sshkube and just use kube-compose directly
$(sshkube init)
kube-compose up
``` 

## Updating your deployment
Just like with docker compose, you can update by running `up` again. It's good practice, however, to make sure that your update won't overwrite something you didn't expect by first running:
```bash
sshkube run kube-compose diff
```

## Rolling back your deployment

If you broke something after an update and want to rollback quickly, you can use:
```bash
sshkube run kube-compose rollback
```

But note that this won't work if you don't maintain separate versions of your docker container, so it's recommended that you do whenver you push. E.g. when updating your container use:
```bash
kube-compose version yourapp-app patch
docker compose build yourapp-app
docker compose push yourapp-app
```

`kube-compose version` makes it easy to version your containers with [semver](https://semver.org/).
