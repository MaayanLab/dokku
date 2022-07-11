# Deploy with Dokku

https://dokku.com/docs/deployment/application-deployment/

```bash
# maybe you want to add this to your .bashrc (replace dokku.maayanlab.cloud with the domain name)
alias dokku="ssh -t dokku@dokku.maayanlab.cloud"

# configure your app on dokku (replace my-app with your app name)
dokku apps:create my-app

# configure your codebase for pushing to dokku
git remote add production dokku@dokku.maayanlab.cloud:my-app

# push app to dokku
git push -u production main

# configure https support for your app (only after first deploy)
dokku letsencrypt:enable my-app
```

## Updating your deployment

With your github repo setup, after making new commits you can update the dokku deployment by simply running
```bash
git push -u production main
```

## Rolling back your deployment

If you broke something and want to rollback, you can use git for this
```bash
# checkout the working code (e.g. HEAD~1 would be the last commit, alternatively locate the commit hash of the working code)
git checkout <working-commit>
git push -u production main --force
# go back to main
git checkout main
```

## Deploying a docker image directly from dockerhub (Advanced)

<https://dokku.com/docs/deployment/methods/git/#initializing-an-app-repository-from-a-docker-image>

Dokku can initialize the git repo for you if all you want to do is deploy an existing docker image on dockerhub. After creating the app it's:

```bash
dokku git:from-image my-app dockerhuborg/some-docker-image
```
