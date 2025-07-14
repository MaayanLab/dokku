# Common Deployment Issues and their Solutions

We've created and maintain this list of common deployment issues people experience since errors can sometimes be cryptic.

## sshkube connection issues
This can have a variety of symptoms:
- nothing is happening after running a command for a long time
- `connection failed` or `TLS handshake timeout` or other related error messages

This is caused because the proxy set up by sshkube is broken but not stopped.

This can be fixed with `sshkube kill-server` then try running your command again.

## platform mismatch
Something along the lines of: `exec format error`

This is caused when the CPU architecture of your machine is different from our cluster (x86), a common example are the new Mac M1s which are ARM based.

To fix it, the docker container must be built for the x86 cluster architecture, it can be achieved with the following update to your service definition in docker compose:
```diff
 services:
   # ...
   yourapp-app:
     build: .
     image: yourusername/yourimage:0.1.0
+    platform: linux/amd64
     # ...
```

You will then have to build and push it again.
