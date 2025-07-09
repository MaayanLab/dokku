# MinIO (S3)

[MinIO](https://min.io/) offers open source S3 compatible object storage, thier solution is very advanced and can scale the way AWS native S3 can across many nodes, alternatively it works just as well on a single system with the added benefit of coming with a easy-to-use user interface that can also be used to manage access controls.

See [tests/minio](https://github.com/MaayanLab/dokku/tree/kube-compose/tests/minio) for complete template.

## Adding minio to your app's docker-compose.yaml

```yaml
services:
  # ...
  yourapp-minio:
    image: quay.io/minio/minio
    pull_policy: missing
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
    - MINIO_ROOT_USER=minio
    # this should be in your .env file and set to a long random string
    - MINIO_ROOT_PASSWORD
    ports:
    - target: 9000
      published: 9000
      x-kubernetes:
        annotations:
          maayanlab.cloud/ingress: https://s3.yourapp.k8s.dev.maayanlab.cloud
    - target: 9001
      published: 9001
      x-kubernetes:
        annotations:
          maayanlab.cloud/ingress: https://console.s3.yourapp.k8s.dev.maayanlab.cloud
    volumes:
    - yourapp-minio-data:/data

volumes:
  yourapp-minio-data:
    x-kubernetes:
      size: 1Gi
      class: local-path
```


## Accessing the database in your app

The database will be accessible at the hostname corresponding to your service name, but it's best practice to set up an environment variable to specify the location. For example, in python:

- `.env`:
  ```
  # so you can test accessing the database locally
  S3_URL=http://minio:YOURMINIO_PASSWORD@localhost:9000/yourbucket
  PUBLIC_S3_URL=http://localhost:9000/yourbucket
  ```
- `docker-compose.yaml`:
  ```yaml
  services:
    yourapp-app:
      environment:
      # so your app container goes to the right location, **NOT localhost**
      - S3_URL=http://minio:${MINIO_ROOT_PASSWORD}$@yourapp-minio:9000/yourbucket
      - PUBLIC_S3_URL=https://s3.yourapp.k8s.dev.maayanlab.cloud
  ```
- `app.py`:
  ```python
  import os
  import io
  import json
  import dotenv
  from minio import Minio
  from urllib.parse import urlparse

  dotenv.load_dotenv()

  # connect to db
  S3_URL_parsed = urlparse(os.environ['S3_URL'])
  s3 = Minio(
    f"{S3_URL_parsed.hostname}:{S3_URL_parsed.port}",
    access_key=f"{S3_URL_parsed.username}",
    secret_key=f"{S3_URL_parsed.password}",
    secure=S3_URL_parsed.scheme == 'https',
  )

  # create the bucket if it doesn't exist
  bucket, _, _ = S3_URL_parsed.path[1:].partition('/')
  if not s3.bucket_exists(bucket):
    s3.make_bucket(bucket)
    # enable anonymous downloading of files in this bucket
    s3.set_bucket_policy(bucket, json.dumps({
      'Version': '2012-10-17',
      'Statement': [
        {'Effect': 'Allow', 'Principial': {'AWS': '*'}, 'Action': 's3:GetBucketLocation', 'Resource': f"arn:aws:s3:::{bucket}"},
        {'Effect': 'Allow', 'Principial': {'AWS': '*'}, 'Action': 's3:GetObject', 'Resource': f"arn:aws:s3:::{bucket}/*"},
      ],
    }))
    # create a file
    content = b'Hello World!'
    s3.put_object(bucket, 'test.txt', io.BytesIO(content), len(content), content_type='plain/text')
    print(f"File available at <{os.environ['PUBLIC_S3_URL']}/test.txt>")

  # ... use s3 in your app deal with files ...
  ```
