# Ma'ayan Lab Dokku Server

## What is Dokku

[Dokku](https://dokku.com/) is an open source lightweight Platform as a Service (PaaS) implementation designed to run on a single host and be operable over ssh. It is inspired by and re-uses developments from the [Heroku](https://www.heroku.com/) platform. Fundamentally, the basic idea is to git push your website to it and have it running online, retaining the benefits of git (easy rollback) and reducing the effort it takes to get a web application online.

## What is this?

The real [dokku docs](https://dokku.com/) are not bad, but administrative side of things and user side of things is a bit intertwined likely making it difficult for someone who just wants to deploy their app to our dokku server.

These opinionated docs try to capture the main parts necessary for administration (server maintenance side of things) and users side (people deploying apps) respectively.

- [User Guide](./user/00-intro.md)
- [Administrator Guide](./administration/00-intro.md)

## Contributions

If you run into issues figuring out how to use dokku or there are gaps in these docs, do consider contributing to this user guide on github either by [submitting an issue](https://github.com/MaayanLab/dokku/issues) or by writing a [pull request](https://github.com/MaayanLab/dokku/pulls).

## User Changelog

The gist of the changes you should be aware of if you're coming from `dokku.maayanlab.cloud` are detailed here:

- [Access docs](./user/10-access.html#configure-access) now require a additional config step, you'll need to review this
  to access the new server.
- [Configuring a repo](./user/30-deploy.html#from-git-repository) needs to use the new domain name. if you already have the `production` origin set up, you can change it with `git remote set-url production dev.maayanlab.cloud:my-app`
- [Finalizing deployments](./user/30-deploy.html#finalizing-the-deployment) was simplified! `dokku letsencrypt:enable` was replaced with `dokku traefik:enable`. When setting up the proxy, only specify `http:80:your-container-port`.
