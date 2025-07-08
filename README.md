# Ma'ayan Lab Kubernetes

This repository contains opinionated documentation for deploying to the Ma'ayan Lab Kubernetes Cluster. Files are just markdown, and [jupyter-book](https://jupyterbook.org/) is used to turn them into a webpage.

While you can add new files to some of the directories, if you add new directories or new root-level files, they'll need to be added to `_toc.yml`.

## Development

```bash
# install python dependencies
pip install -r requirements.txt

# build html
jupyter-book build .

# the resulting book is in _build/html, the html can be viewed with any static web browser (including just opening _build/html/index.html in your browser)
npx http-server _build/html
```

## Deployment

This can be deployed directly to the Cluster, see [deploy docs](./user/50-deploy) for that, but essentially it's just:

```bash
docker compose build
docker compose push
kube-compose up
```
