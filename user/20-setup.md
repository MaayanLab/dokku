# Setup Repo for Dokku Deployment

Dokku can be used to deploy an app in several ways:
- A repository with Dockerfile https://dokku.com/docs/deployment/builders/dockerfiles/
  - normal deployment, `Dockerfile` should be at the root of the repo
    note that `EXPOSE <portname>` is necessary for the port to be autodetected and proxied.
- "Heokuish Buldpack" https://dokku.com/docs/deployment/builders/herokuish-buildpacks/
  - if no Dockerfile is present, it uses heoku's "buildpacks" which supports most common language mechanisms
    of running, e.g requirements.txt file in python.
    The "run" command is defined in a root `Procfile` which looks like
    ```Procfile
    # <process name>: <command>
    web: python run.py
    ```
- A docker image https://dokku.com/docs/deployment/methods/git/#initializing-an-app-repository-from-a-docker-image
  - dokku git:from-image my-app dockerhuborg/some-docker-image
