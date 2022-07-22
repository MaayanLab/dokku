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
# AWS account with read/write permissions to the bucket
#  only necessary if using aws s3
export AWS_ACCESS_KEY_ID=<access_key_id>
export AWS_SECRET_ACCESS_KEY=<secret_access_key>
# actual repository
export RESTIC_REPOSITORY=s3:s3.amazonaws.com/<some-bucket>/dokku-backup/
# some secure password to use for encrypting the backups, save somewhere else
export RESTIC_PASSWORD=<encryption_password>
```

### Initializing a Backup Repository

```bash
# initialize backup repository **first time run only**
restic init
```

### Creating regular backups

This should be done as part of a daily/weekly cron-job.

- `/root/dokku-backup.sh`
  ```bash
  #!/bin/bash

  # TODO: fill in from before
  export AWS_ACCESS_KEY_ID=
  export AWS_SECRET_ACCESS_KEY=
  export RESTIC_REPOSITORY=
  export RESTIC_PASSWORD=

  # backup relevant directories
  restic backup \
    /home/dokku \
    /var/lib/dokku/config \
    /var/lib/dokku/data \
    /var/lib/dokku/services \
    /var/lib/dokku/plugins

  # prune backups on a schedule
  restic forget \
    --prune \
    --keep-last 10 \
    --keep-daily 7 \
    --keep-weekly 4 \
    --keep-monthly 12 \
    --keep-yearly 5

  # check for integrity issues on random subset
  restic check \
    --read-data-subset=1/20
  ```
- `sudo crontab -e`
  ```crontab
  # daily at 3am
  0 3 * * * systemd-cat -t "dokku-backup" /root/dokku-backup.sh
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
