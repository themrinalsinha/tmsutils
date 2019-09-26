from os                  import walk
from glob                import glob
from os.path             import (isdir, exists, join, dirname,
                                 basename, abspath)

from boto3               import client
from botocore.client     import Config
from botocore.exceptions import ClientError

class S3(object):
    '''
    S3 class for S3 Compatable storages
    '''
    def __init__(self, access_key, secret_key, bucket, region, endpoint=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket     = bucket
        self.region     = region
        self.endpoint   = endpoint
        self.connection = self.get_connection()

    def get_connection(self):
        '''
        Returns connection object based on given data, by default
        endpoint url points to aws s3 and given region.

        Endpoint and region for wasabi s3 storage.
        eg: endpoint: 'https://s3.wasabisys.com'
            region  : 'us-east-1'
        '''
        return client(service_name          = 's3',
                      aws_access_key_id     = self.access_key,
                      aws_secret_access_key = self.secret_key,
                      region_name           = self.region,
                      endpoint_url          = self.endpoint,
                      config                = Config(signature_version='s3v4'))

    def file_exists(self, file_key, bucket=self.bucket):
        try:
            self.connection.head_object(Bucket=bucket, key=file_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            return e

    def get_temperory_link(self, file_key, bucket=self.bucket, expire=300):
        '''
        Generating temperory download link for given file_key
        default expire timeout is 300 seconds = 10 min
        '''
        if self.file_exists(file_key):
            return self.connection.generate_presigned_url(
                            ClientMethod = 'get_object',
                            Params       = {'Bucket': bucket, 'Key': file_key},
                            ExpiresIn    = expire)
        return False

    def upload(self, file_path, bucket=self.bucket):
        '''
        Upload the given file or directory to given S3 bucket
        if file_path is a directory it will zip it and then upload it
        '''
        if isdir(file_path):
            for root, _, _filenames in walk(file_path):
                for filename in _filenames:
                    file_key = join(root, filename)
                    abs_path = abspath(file_key)
                    self.connection.upload_file(abs_path, bucket, file_key)
            return True

        elif not exists(file_path):
            return False

        file_key = basename(file_path)
        self.connection.upload_file(file_path, bucket, file_key)
        return True

