#!/bin/bash

export DOKKU_CMD="sudo dokku"

dokku-add-ssh-from-github() {
  username=$1
  let n=0
  curl "https://github.com/${username}.keys" \
    | while read pubkey; do
      echo "$pubkey" | $DOKKU_CMD ssh-keys:add "github-${username}-${n}";
      let n=$n+1;
    done
}

dokku-remove-ssh-from-github() {
  username=$1
  dokku ssh-keys:list \
    | gawk -v username=$username 'match($0, /NAME="([^"]+)"/, m) && m[1] ~ "^github-" username { print m[1] }' \
    | while read full_username; do
      $DOKKU_CMD ssh-keys:remove "$full_username";
    done
}

if [ "${BASH_SHOURCE[0]}" -ef "$0" ]; then
  CMD=$1
  shift
  if [ "$CMD" == "add" ]; then
    dokku-add-ssh-from-github $@
  elif [ "$CMD" == "remove" ]; then
    dokku-remove-ssh-from-github $@
  else
    echo "Usage: $0 <add | remove> <github-username>"
    exit 1
  fi
fi
