import uuid
import json
import boto3
import os
import csv

class S3(object):

    def save_to_bucket(self, filepath, key):
        file = open(filepath.name, "rb")
        file.seek(0)
        s3     = boto3.resource('s3')
        bucket = s3.Bucket(os.environ['bucket'])
        bucket.put_object(
            ContentType='text/csv',
            Key=key,
            Body=file,
        )
        file.close()
        body = {
            "bucket": os.environ['bucket'],
            "path": key,
        }
        return {
            "body": json.dumps(body)
        }

    def retrieve_file(self, filename):
        s3_client = boto3.client('s3')
        tmp_name  = '/tmp/' + str(uuid.uuid4())
        s3_client.download_file(os.environ['bucket'], filename, tmp_name)
        content   = csv.reader(open(tmp_name))
        return content