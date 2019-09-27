from os                  import getcwd, makedirs
from glob                import glob
from os.path             import isdir, exists, join, dirname, basename

from boto3               import client
from botocore.client     import Config
from botocore.exceptions import ClientError

class S3(object):
    '''
    S3 class for S3 Compatable storages
    '''
    def __init__(self, access_key, secret_key, bucket, region, endpoint=None, directory=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket     = bucket
        self.region     = region
        self.endpoint   = endpoint
        self.directory  = directory
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

    def file_exists(self, file_key, bucket=None):
        '''
        Function to check if given key exists in given bucket
        '''
        try:
            self.connection.head_object(Bucket=bucket or self.bucket, Key=file_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            return e

    def get_temperory_link(self, file_key, bucket=None, expire=300):
        '''
        Generating temperory download link for given file_key
        default expire timeout is 300 seconds = 10 min
        '''
        if self.file_exists(file_key):
            return self.connection.generate_presigned_url(
                            ClientMethod = 'get_object',
                            Params       = {'Bucket': bucket or self.bucket, 'Key': file_key},
                            ExpiresIn    = expire)
        return False

    def upload(self, file_path=None, bucket=None):
        '''
        Upload the given file or directory to given S3 bucket, if the filepath is a directory
        it will upload the entire directory maintaining it's directory structure or if it is
        a file it will just upload the file.

        TODO: add zip support - compress folder to zip and then upload.
        '''
        file_path = file_path or self.directory
        file_path = file_path.rstrip('/')
        bucket    = bucket or self.bucket

        if isdir(file_path):
            _skip     = len(dirname(file_path))
            _basename = basename(file_path)
            all_files = glob(join(file_path, '**/*'), recursive=True)
            all_files = [f for f in all_files if not isdir(f)]
            for _file in all_files:
                file_key = _file[_file.index(_basename, _skip):]
                self.connection.upload_file(_file, bucket, file_key)
            return True

        elif not exists(file_path):
            return False

        file_key = basename(file_path)
        self.connection.upload_file(file_path, bucket, file_key)
        return True

    def download(self, file_key=None, folder_prefix=None, download_dir=None, bucket=None):
        '''
        Download given file based on given file_key or prefix (in case of a folder)
        it will either download everything to download_dir or current directory

        Argument:
            file_key - in case of downloading only one file
            folder_prefix - in case of donloading entire folder from bucket with pattern
                eg: ORD123/ or ORD123/invoices/
        '''
        download_dir = download_dir or self.directory or getcwd()
        bucket       = bucket or self.bucket

        if folder_prefix:
            bucket_data = self.connection.list_objects(Bucket=bucket, Prefix=folder_prefix).get('Contents')
            if bucket_data:
                download_keys = [x.get('Key') for x in bucket_data]
                for key in download_keys:
                    download_path = join(download_dir, key)
                    if not exists(dirname(download_path)):
                        makedirs(dirname(download_path))
                    self.connection.download_file(bucket, key, download_path)
                return join(download_dir, folder_prefix)

        elif file_key and self.file_exists(file_key):
            self.connection.download_file(bucket, file_key, join(download_dir, basename(file_key)))
            return join(download_dir, basename(file_key))
        return False
