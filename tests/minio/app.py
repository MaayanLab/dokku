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
