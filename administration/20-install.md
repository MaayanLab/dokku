# Install Dokku Server

Described in this article: <https://dokku.com/docs/getting-started/advanced-installation/> which points to system specific installation.

## Cloud Ubuntu

```bash
wget https://raw.githubusercontent.com/dokku/dokku/master/bootstrap.sh
sudo DOKKU_BRANCH=master bash bootstrap.sh
```

## Baremetal Ubuntu + Vagrant

```bash
# install dependencies
sudo apt update
sudo apt install git vagrant virtualbox
# virtualbox patch
sudo mkdir -p /etc/vbox
sudo tee networks.conf <<< "* 0.0.0.0/0 ::/0"
# useful vagrant plugin for managing disk size
vagrant plugin install vagrant-disksize
# get dokku
git clone https://github.com/dokku/dokku.git
cd dokku
```

Apply the following patch to the Vagrantfile for easy disk resizing:

```diff
--- Vagrantfile.old     2022-08-02 11:28:19.247438313 -0400
+++ Vagrantfile 2022-08-02 12:11:50.112665016 -0400
@@ -4,6 +4,7 @@
 BOX_NAME = ENV["BOX_NAME"] || "bento/ubuntu-18.04"
 BOX_CPUS = ENV["BOX_CPUS"] || "1"
 BOX_MEMORY = ENV["BOX_MEMORY"] || "1024"
+BOX_DISKSIZE = ENV["BOX_DISKSIZE"] || "64GB"
 DOKKU_DOMAIN = ENV["DOKKU_DOMAIN"] || "dokku.me"
 DOKKU_IP = ENV["DOKKU_IP"] || "10.0.0.2"
 FORWARDED_PORT = (ENV["FORWARDED_PORT"] || '8080').to_i
@@ -15,10 +16,18 @@
   make_cmd = "PREBUILT_STACK_URL='#{PREBUILT_STACK_URL}' #{make_cmd}"
 end
 
+disk_resize = <<-SCRIPT
+sudo parted /dev/sda resizepart 1 100%
+sudo pvresize /dev/sda1
+sudo lvextend -l +100%FREE /dev/vagrant-vg/root
+sudo resize2fs /dev/vagrant-vg/root
+SCRIPT
+
 Vagrant::configure("2") do |config|
   config.ssh.forward_agent = true
 
   config.vm.box = BOX_NAME
+  config.disksize.size = BOX_DISKSIZE
 
   config.vm.provider :virtualbox do |vb|
     vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
@@ -55,6 +64,7 @@
       vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
     end
 
+    vm.vm.provision :shell, :run => 'always', :inline => disk_resize
     vm.vm.provision :shell, :inline => "export DEBIAN_FRONTEND=noninteractive && apt-get update -qq >/dev/null && apt-get -qq -y --no-install-recommends install git build-essential >/dev/null && cd /root/dokku && #{make_cmd}"
     vm.vm.provision :shell do |s|
       s.inline = <<-EOT
```

```bash
# provision dokku with vagrant
env \
  BOX_CPUS=4 \
  BOX_MEMORY=16384 \
  BOX_DISKSIZE=64GB \
  DOKKU_IP=10.0.0.2 \
  DOKKU_DOMAIN=dokku.maayanlab.cloud \
  FORWARDED_PORT=8080 \
  vagrant up

# login to dokku
vagrant ssh
```

### Resizing Disk

The disk can be resized by running `vagrant halt` then the `env ... vagrant up` command again with the updated `BOX_DISKSIZE`.

## Baremetal Ingress

In a cloud environment and on a dedicated system, this part is not necessary, but on a system which serves other things an ingress is essential. The simplest way to setup an ingress to serve this and other things is with traefik in a docker-compose. This lets us expose multiple http services on the one port differentiated by the hostname, and can be used for ssh over tls if that is necessary.

- `docker-compose.yml`
  ```yml
  version: '3'
  services:
    ingress:
      image: traefik
      ports:
        - 80:80
        - 443:443
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock
        - ./ingress/traefik.yaml:/etc/traefik/traefik.yaml
        - ./ingress/config:/config
        - ./ingress/data:/data
  ```
- `ingress/traefik.yaml`
  ```yaml
  providers:
    file:
      directory: /config
      watch: true
    docker:
      exposedByDefault: false
  entryPoints:
    web:
      address: :80
    websecure:
      address: :443
  ```
- `ingress/config/dokku-passthrough.yaml`
  ```yaml
  http:
    routers:
      # forward http packets over to the dokku container to be handled
      dokku-http:
        rule: Host(`dokku.maayanlab.cloud`) || Host(`*.dokku.maayanlab.cloud`)
        entryPoints:
          - web
        service: dokku-http
    services:
      dokku-http:
        loadBalancer:
          servers:
            # this is the DOKKU_IP specified in the vagrant install
            - url: "http://10.0.0.2:80/"
  tcp:
    routers:
      # we'll let dokku handle tls
      dokku-https:
        priority: 1
        rule: HostSNIRegexp(`dokku.maayanlab.cloud`, `{subdomain:.+}.dokku.maayanlab.cloud`)
        entryPoints:
          - websecure
        service: dokku-https
        tls:
          passthrough: true
      # only necessary if doing ssh-over-tls -- do tls termination to the ssh port
      dokku-ssh:
        priority: 0
        rule: HostSNI(`ssh.dokku.maayanlab.cloud`)
        entryPoints:
          - websecure
        service: dokku-ssh
        tls: {}
    services:
      dokku-https:
        loadBalancer:
          servers:
            # this is the DOKKU_IP specified in the vagrant install
            - address: 10.0.0.2:443
      # only necessary if doing ssh-over-tls
      dokku-ssh:
        loadBalancer:
          servers:
          # this is the DOKKU_IP specified in the vagrant install
          - address: 10.0.0.2:22

  ```
## Configure Dokku

```bash
# setup domain name
dokku domains:set-global dokku.maayanlab.cloud

# use main instead of master
dokku git:set --global deploy-branch main

# setup traefik auto-tls w/ letsencrypt
sudo dokku plugin:install https://github.com/maayanlab/dokku-traefik.git
dokku config:set --global DOKKU_LETSENCRYPT_EMAIL=your_email@gmail.com
dokku traefik:start
```
