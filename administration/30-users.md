# User administration
```bash
dokku ssh-keys:add username [path_to_key]
dokku ssh-keys:list
dokku ssh-keys:remove username
```

## Managing users using github pubkeys
These functions were added to a script {download}`dokku-github-keys.sh` which can be installed on the host serving dokku for convenience.

```bash
# github.com serves user public keys, so we can just fetch them from there by github username
#  and register them with dokku. users may have multiple keys so we add them one by one.
dokku-add-ssh-from-github() {
  username=$1
  let n=0
  curl "https://github.com/${username}.keys" \
    | while read pubkey; do
      echo "$pubkey" | sudo dokku ssh-keys:add "github-${username}-${n}";
      let n=$n+1;
    done
}

# to revoke a user added via github, this script simply removes `github-${username}` prefixed entries
dokku-remove-ssh-from-github() {
  username=$1
  sudo dokku ssh-keys:list \
    | gawk -v username=$username 'match($0, /NAME="([^"]+)"/, m) && m[1] ~ "^github-" username { print m[1] }' \
    | while read full_username; do
      sudo dokku ssh-keys:remove "$full_username";
    done
}

dokku-add-ssh-from-github gh-username
dokku-remove-ssh-from-github gh-username
```
