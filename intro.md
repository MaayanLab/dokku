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
