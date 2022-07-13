# Ma'ayan Lab Dokku Server

Currently running at <https://dokku.maayanlab.cloud/>.

This repository contains documentation for the Ma'ayan Lab Dokku Server. Files are just markdown, and [jupyter-book](https://jupyterbook.org/) is used to turn them into a webpage.

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

This can be deployed *with dokku itself*, see [dokku docs](./user/30-deploy.md) for that. But even without dokku it's just a matter of building the Dockerfile.

```bash
# Build docker file, a python builder builds the html
#  and the final image is just an nginx-served static site
docker build -t maayanlab/dokku .

# nginx serves the static site on port 80
docker run -p 80:80 -it maayanlab/dokku
```
