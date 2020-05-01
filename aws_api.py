import boto3


class AWSS3Client(object):
    def __init__(self, s3_bucket, profile_name):
        """
            The created object allows to interact with the given bucket of AWS:S3.
            Args:
                profile_name (str): the name of the AWS profile in your '~/.aws/config' file
                s3_bucket    (str): the bucket to interact with
        """
        s = boto3.Session(profile_name=profile_name)
        self.resource = s.resource(service_name='s3')
        self.bucket = self.resource.Bucket(s3_bucket)

    def upload(self, file_name):
        self.bucket.upload_file(file_name, file_name, ExtraArgs={'ACL': 'public-read', 'CacheControl': "private,max-age=0,no-cache,must-revalidate", 'ContentType': 'text/html'})
