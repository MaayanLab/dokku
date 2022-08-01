# Dokku Application Configuration

After creating your app, before or after you've deployed it you can configure it with several dokku commands.

## Environment variables

It's often good practice to use a `.env` file with environment variables for your app in several situations. Examples include:
- database credentials
- url prefixes

It is ideal to include a `.env.example` file in your repo, potentially with comments about what the values should be in cases where they are omitted, but leave the `.env` out of the repository and add it to `.gitignore` to prevent accidental commit.

Packages exist for loading environment variables from `.env` automatically like the `python-dotenv` package.

## Environment variables on Dokku

When you launch your app on dokku, adding the environment configuration is an additional step:

```bash
# replace my-app with your app name
#  each environment KEY=VALUE pair can be provided on the args
# this will apply the config and restart your app
dokku config:set my-app "SOME_KEY=SOME_VALUE" "SOME_KEY2=SOME_VALUE2"

# review environment variables for your app
dokku config:show my-app

# unset a previously set environment variable
dokku config:unset my-app SOME_KEY
```
