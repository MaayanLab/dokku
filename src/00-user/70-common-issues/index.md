# Common Deployment Issues and their Solutions

We've created and maintain this list of common deployment issues people experience since errors can sometimes be cryptic.

## sshkube connection issues
This can have a variety of symptoms:
- nothing is happening after running a command for a long time
- `connection failed` or `TLS handshake timeout` or other related error messages

This is caused because the proxy set up by sshkube is broken but not stopped.

This can be fixed with `sshkube kill-server` then try running your command again.

