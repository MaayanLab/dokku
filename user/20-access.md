# Get Access to the Cluster

You access our cluster through an ssh server. To securely access that ssh server, you need an ssh key-pair which comes with a private and public part. The public part can be shared with others and ensures your identity can be verified (given that you're the only holder of the private key).

For management simplicity, we expect your public key to be associated with your github account, that way we can easily pull the key from there.

## Generating a ssh key-pair

For more information, see [github's docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) on the subject.

Only necessary if you haven't already done this, it is reasonable to reuse an existing ssh key-pair.

In your terminal:
```bash
# generate the key, press enter several times to accept defaults until the terminal returns
#  no need to specify a password it's not necessary if only you use your system and can be annoying
ssh-keygen -t ed25519

# output your public key and copy it from the terminal into your clipboard
#  it looks like `ssh-ed25519 AAAAC3Nza....A username@hostname`
cat ~/.ssh/id_ed25519.pub
```

## Adding the ssh public key to your github account

For more information, see [github's docs](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) on the subject.

On github, in Settings > Access > SSH and GPG keys, add New SSH Key, and paste the key in the key section, name it whatever and add it.

## Request access from an administrator
The lab administrator can, using your github username, give you access to the cluster. A command they run will authorize your github public key allowing you to run access a bastian host enabling access to the cluster. Once requested, proceed to the next step since there is some system setup required.

## Configure access to the cluster
Once your access has been confirmed by a system administrator, you should be able to successfully configure access to the cluster with the following command:

```bash
sshkube install -s ssh.k8s.dev.maayanlab.cloud -u your-github-username
```

This will report `Success` if it worked, if not, let us know so we can figure out why.

## Next Steps

[Setup your codebase](./30-setup-code.md) to be deployable.
