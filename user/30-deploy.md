# Deploy with Dokku

Here we walk through the basics of creating an app in dokku and pushing your app to it. Notably it's necessary that your code-base is already set up as a [git](https://git-scm.com/) repository. All examples is `my-app`, this should be replaced with the app you're trying to manage.

For more information, see the [application-deployment](https://dokku.com/docs/deployment/application-deployment/) docs on dokku.

## Deploying

```bash
# configure your app on dokku (replace my-app with your app name)
dokku apps:create my-app
```

### From Git Repository

```bash
# configure your codebase for pushing to dokku
#  must be executed in the directory of your repository
git remote add production dev.maayanlab.cloud:my-app

# push app to dokku, you should see messages about the deployment
#  including posibly an error message if something went wrong.
git push -u production main
```

Proceed with finalizing the deployment.

### Directly from dockerhub (Advanced)

For more information, see [dokku's docs](https://dokku.com/docs/deployment/methods/git/#initializing-an-app-repository-from-a-docker-image) on the subject.

Dokku can initialize the git repo for you if all you want to do is deploy an existing docker image on dockerhub. After creating the app it's:

```bash
# replace my-app and org/image with the app name and docker image respectively
dokku git:from-image my-app org/image
```

Proceed with finalizing the deployment.

## Finalizing the deployment

```bash
# overwrite any broken proxy config dokku inferred (replace 5000 with the port your container serves on)
dokku proxy:clear-config my-app
dokku proxy:ports-set my-app 'http:80:5000'

# your app is automatically deployed at https://my-app.dev.maayanlab.cloud
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
