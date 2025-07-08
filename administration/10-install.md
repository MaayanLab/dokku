These are the base services for the cluster:
```bash
# install install some ingress provider
# install cert-manager with letsencrypt
helm install maayanlab/kubernetes-auto-ingress kubernetes-auto-ingress --set watchNamespace="*"
# install some storage provider
```

```yaml
# custom registry
services:
  registry:
    image: registry:2
    ports:
    - 5000
    volumes:
      registry:/var/lib/registry
    x-kubernetes:
      annotations:
        maayanlab.cloud/ingress: https://registry.dev.maayanlab.cloud
        nginx.ingress.kubernetes.io/auth-type: basic
        nginx.ingress.kubernetes.io/auth-secret: registry-basicauth
        nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - Maayan Lab'

volumes:
  registry:

x-kubernetes:
  name: registry
  namespace: registry
  secrets:
    registry-basicauth:
      auth: maayanlab:$apr1$2dr8b6PD$rSfb.FEz2GqC9LMUUMB2U1
```

For all locally deployed images:
```yaml
service:
  image: docker.dev.maayanlab.cloud/yourapp/app

x-kubernetes:
  name: yourapp
  namespace: yourapp
  secrets:
    registry-token:
      .dockerconfigjson: {"auths":{"registry.dev.maayanlab.cloud":{"auth":"bWFheWFubGFiOnN5c3RlbXNiaW9sb2d5Cg=="}}}

  serviceaccounts:
    default:
      imagePullSecrets: registry-token
```
