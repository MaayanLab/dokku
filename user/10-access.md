# Get Access to the Dokku Server

Dokku is ultimately an ssh server, dokku commands run on that server over ssh and git push happens over ssh as well. To securely access an ssh server, you need an ssh key-pair which comes with a private and public part. The public part can be shared with others and ensures your identity can be verified (given that you're the only holder of the private key).

For management simplicity, we expect your public key to be associated with your github account, that way we can easily pull the key from there. For more information about associating an ssh key with your github account.

## Generating a ssh key-pair

For more information, see [github's docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) on the subject.

Only necessary if you haven't already done this, it is reasonable to reuse an existing ssh key-pair.

In your terminal:
```bash
# generate the key, press enter several times to accept defaults until the terminal returns
#  no need to specify a password it's not necessary if only you use your system and can be annoying
ssh-keygen -t rsa -b 4096

# output your public key and copy it from the terminal into your clipboard
#  it looks like `ssh-rsa AAAAB3NzaC1...UQ== username@hostname`
cat ~/.ssh/id_rsa.pub
```

## Adding the ssh public key to your github account

For more information, see [github's docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) on the subject.

On github, in Settings > Access > SSH and GPG keys, add New SSH Key, and paste the key in the key section, name it whatever and add it.

## Request access from an administrator

The lab administrator of dokku can, using your github username, give you access to dokku. A command they run will authorize your github public key allowing you to run dokku commands on the server and push to it. You will also receive the dokku domain name, e.g. `dev.maayanlab.cloud` -- this is where you will push and apps will automatically be visible at `<app-name>.dev.maayanlab.cloud`.

## Configure access

To simplify ssh access, it's best to add a host to your `~/.ssh/config`. The remaining articles assume you have performed this step.

Note: This script writes it directly to `.ssh/config`, alternatively you can modify the file directly.

```bash
cat >> ~/.ssh/config << EOF
Host dev.maayanlab.cloud
  ProxyCommand openssl s_client -servername ssh.dev.maayanlab.cloud -connect ssh.dev.maayanlab.cloud:443 -quiet
  IdentityFile ~/.ssh/id_rsa
  IdentitiesOnly yes
  User dokku
EOF
```

Next you'll want to make sure you always have access to the `dokku` command, you can do so by adding an alias to your `.bashrc` which runs on terminal startup.

```bash
echo 'alias dokku="ssh -t dev.maayanlab.cloud"' >> ~/.bashrc
```

## Verify access

Once you've been given access and have configured things, you can confirm that it's working with the dokku command:

```bash
# should connect to the server, print the dokku help, and disconnect
dokku
```
