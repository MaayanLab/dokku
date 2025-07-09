# Setup System for Kubernetes Deployment

## Install Required Programs
- sshkube: a cli our team maintains for simplifying kubernetes access
- kube-compose: a cli our team maintains for simplifying kubernetes deployment
- python/pipx: required to install/run our cli
- docker: build and run containers locally
- docker-compose: manage multiple containers operating together
- kubectl: a CLI for kubernetes
- helm: a package manager for kubernetes

### Mac OS X
It's recommended that you install [homebrew](https://brew.sh/) on your mac to make installation easier and more consistent.

After instlaling homebrew, in a terminal, run the following commands:

```bash
brew update
brew install git pipx kubernetes-cli helm
brew install --cask docker-desktop

pipx ensurepath
pipx install sshkube kube-compose
```

### Linux
In a terminal, run the following commands:

```bash
sudo apt-get update -y
sudo apt-get install -y git docker docker-compose pipx kubectl
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

pipx ensurepath
pipx install sshkube kube-compose
```

### Windows
WSL is recommended with the linux instructions, but we do try to support native windows, let us know if you experience issues.

It's recommended that you install [scoop](https://scoop.sh/) on your windows machine to make installation easier and more consistent.

Afer installing scoop, in a terminal, run the following commands:
```bash
scoop bucket add main
scoop install git docker docker-compose pipx kubectl helm

pipx ensurepath
pipx install sshkube kube-compose
```

## Create a Github Account
You will need a [github](https://github.com/) account both to manage source code and to register a ssh public key.

## Login to Dockerhub
Besides github which you should have already set up by now. You'll also need an account on [Dockerhub](https://hub.docker.com/) to publish your own containers. Once setup you can login to dockerhub with

```bash
docker login
```
