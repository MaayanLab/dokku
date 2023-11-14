# MinIO (S3)

[MinIO](https://min.io/) offers open source S3 compatible object storage, thier solution is very advanced and can scale the way AWS native S3 can across many nodes, alternatively it works just as well on a single system with the added benefit of coming with a easy-to-use user interface that can also be used to manage access controls.

## What's this for?

MinIO is the ideal place to store static files like data dumps which don't belong in the source code (perhaps they are too big) but are necessary for your app.

Files stored in minio which are configured to have public-read permissions are accessible at:

- `s3://<bucket-name>/<file/path>`
  - given that the endpoint is configured to https://minio.dev.maayanlab.cloud
- `https://minio.dev.maayanlab.cloud/<bucket-name>/<file/path>`

## Getting access

To get credentials for the minio server, contact an administrator to get access.

The MinIO S3 server is available at:
- https://minio.dev.maayanlab.cloud

Your web browser will redirect you to the console where you can upload and manage files. Alternatively most S3 compatible clients can access minio with the proper endpoint, for example [rclone](https://rclone.org/s3/).
