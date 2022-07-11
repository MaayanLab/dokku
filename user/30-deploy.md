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
