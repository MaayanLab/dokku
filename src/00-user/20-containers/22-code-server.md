# Setup VSCode Server on the Cluster

[Code Server](https://github.com/coder/code-server) is a web-based environment for running vscode.

Our cluster has lots of storage and memory and runs 24/7 so it might be a more ideal place to run experiments than on your laptop.

## Creating a code server service

In a blank directory, create a file:
- `docker-compose.yaml`:
  ```yaml
  services:
    code-server:
      image: lscr.io/linuxserver/code-server:latest
      pull_policy: missing
      restart: unless-stopped
      ports:
      - 8443:8443
      volumes:
      - code-data:/config

  volumes:
    code-data:
      x-kubernetes:
        size: 1Gi
        class: local-path

  x-kubernetes:
    name: code
  ```

## Running VSCode Server Locally

Honestly you should probably just run [VSCode](https://code.visualstudio.com/) the desktop environment, if you want to run locally.

## Run VSCode Server on the Cluster

In the same directory, you can launch the same code server on the cluster with:

```bash
kube-compose up
```

Now that it's running on the cluster, to access it you'll need to port forward:
```bash
# this command stays running to keep the port forwarding open
sshkube run kube-compose port-forward code-server 8443
```

Now visit <http://localhost:8443> to access your vscode server running on the cluster.

Top stop it run
```bash
# add -v to delete the volume
sshkube run kube-compose down
```
