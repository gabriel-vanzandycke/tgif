#!/usr/bin/env python
import os
import datetime
import schedule
import time
import boto3
from holidays import official_tgif, get_holidays



target = 4 # 4= friday

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

s3_client = AWSS3Client("auie", "gva@DEV")

def replace(src_filename, dst_filename, src_string, dst_string):
    # Read in the file
    with open(src_filename, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(src_string, dst_string)

    # Write the file out again
    with open(dst_filename, 'w') as file:
        file.write(filedata)


def job(*_): # argument unused for now
    holidays = get_holidays()
    days, exponent = official_tgif(holidays)
    replace("tgif.html.template", "tgif.html", "#DAYS#", str(days))
    replace("tgif.html.template", "tgif.html", "#EXPONENT#", str(exponent))
    s3_client.upload("tgif.html")

schedule.every().day.at("07:00").do(job, None)
job()
while True:
    schedule.run_pending()
    time.sleep(60*60) # check schedule every hour

