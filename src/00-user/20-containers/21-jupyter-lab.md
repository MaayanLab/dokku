# Setup Jupyter Lab on the Cluster

[Jupyter Lab](https://jupyterlab.readthedocs.io/en/latest/) is a web-based environment for running jupyter notebooks. It's frequently run locally but can also be run on another system so that underlying computation happens on that system.

Our cluster has lots of storage and memory and runs 24/7 so it might be a more ideal place to run experiments than on your laptop.

See [tests/jupyter](https://github.com/MaayanLab/dokku/tree/kube-compose/tests/jupyter) for complete template.

## Creating a jupyter lab service

In a blank directory, create a file:
- `docker-compose.yaml`:
  ```yaml
  services:
    jupyter-lab:
      image: maayanlab/jupyter-base-notebook:1.0.0
      pull_policy: missing
      restart: unless-stopped
      command: start-notebook.py --NotebookApp.token=''
      ports:
      - 8888:8888
      volumes:
      - jupyter-data:/home/jovyan/work

  volumes:
    jupyter-data:
      x-kubernetes:
        size: 1Gi
        class: local-path

  x-kubernetes:
    name: jupyter
  ```

## Running Jupyter Lab Locally

In the directory you created, you can run jupyter lab locally with:

```bash
# run jupyter lab locally
docker compose up -d
```

Now visit <http://localhost:8888> to access your jupyter lab server.

Top stop it run (required if proceeding to the next step of this tutorial)
```bash
# add -v to delete the volume
docker compose down
```

## Run Jupyter Lab on the Cluster

In the same directory, you can launch the same jupyter lab on the cluster with:

```bash
sshkube run kube-compose up
```

Now that it's running on the cluster, to access it you'll need to port forward:
```bash
# this command stays running to keep the port forwarding open
sshkube run kube-compose port-forward jupyter-lab 8888
```

Now visit <http://localhost:8888> to access your jupyter lab server running on the cluster.

Top stop it run
```bash
# add -v to delete the volume
sshkube run kube-compose down
```
