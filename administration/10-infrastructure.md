# Infrastructure for Dokku

Dokku is just a program but must run on some system obviously. It's not a "real" production system since everything must run on one host, in practice it will probably become a mess as well. It is probably convenient for summer intern rapid deployment iterations, though perhaps just giving them a small dedicated cluster in rancher could work just as well.

## Provisioning

At the time of writing, the only real "scheduler" uses docker. For this reason, running it *in* docker as part of kubernetes or something is not a great idea since it needs access to the docker process. In light of this, the two main options I would recommend are:

- provision a dedicated host on a cloud to serve this (install guide has some cloud-specific instructions)
- run it in a virtual machine, for example, with vagrant which is supported by dokku

## Network setup

### Firewall

Ports 22 (ssh), 80 (http), and 443 (https) must be accessible.

### DNS

A hostname should be configured along with a wildcard CNAME record:

```raw
record_type   name                      value
A             dokku.maayanlab.cloud     your.host.ip.addr
CNAME         *.dokku.maayanlab.cloud   dokku.maayanlab.cloud
```

This is convenient as apps will be mounted at `app.dokku.maayanlab.cloud`
