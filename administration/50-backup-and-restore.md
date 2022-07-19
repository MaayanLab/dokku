# Backup and Restoration

[Restic](https://restic.net/) is a fast and versitile tool with first-class support for multi-threading and can backup to any target whether it's a local disk, sftp, s3 or some arbitrary rclone backend. Backed up files are de-duplicated at a chunk-level and stored by content hash providing easy integrity checking. For more information, see the restic docs.

As long as important files are kept in the dokku prescribed places, everything can be easily restored, those places are:
- `/home/dokku`: repos people push
- `/var/lib/dokku/config`: dokku global config
- `/var/lib/dokku/data`: persistent app storage
- `/var/lib/dokku/services`: dokku service storage
- `/var/lib/dokku/plugins`: dokku plugin storage

## Backup

### Configuring Backup Target

```bash
export AWS_ACCESS_KEY_ID=<access_key_id>
export AWS_SECRET_ACCESS_KEY=<secret_access_key>
export RESTIC_REPOSITORY=s3:s3.amazonaws.com/<some-bucket>/dokku-backup/
export RESTIC_PASSWORD=<encryption_password>
```

### Initializing a Backup Repository

```bash
# initialize backup repository **first time run only**
restic init
```

### Creating regular backups

This should be done as part of a cron-job, perhaps daily or weekly.

```bash
# create a backup
restic backup /home/dokku /var/lib/dokku/config /var/lib/dokku/data /var/lib/dokku/services /var/lib/dokku/plugins
# check a random 5% of all data integrity to identify corrupt backups before they become a problem
restic check --read-data-subset=1/20
# see restic docs for `restic forget` which can be used to prune backups
```

## Restoration

### Listing snapshots

```bash
restic snapshots
```

### Review backups through mount

```bash
mkdir -p /mnt/restic
restic mount /mnt/restic
```

In another terminal (or even in a file manager GUI), you can browse snapshots and copy things that should be restored
```bash
ls /mnt/restic
```

### Restore from a backup in-place (Not Recommended)

```bash
restic restore <snapshot-id> --target /
```
