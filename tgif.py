#!/usr/bin/env python
import os
import datetime
import schedule
import time
import boto3
import shutil
from holidays import official_tgif, get_holidays
from slack import WebClient
from aws_api import AWSS3Client

target = 4 # 4= friday

s3_client = AWSS3Client("auie", "gva@DEV")
slack_client = WebClient(token=os.environ["SLACK_API_TOKEN"])

def replace(filename, src_string, dst_string):
    # Read in the file
    with open(filename, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(src_string, dst_string)

    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)


exponent_table = {
    0: "⁰",
    1: "¹",
    2: "²",
    3: "³"
}

def job(*_): # argument unused for now
    holidays = get_holidays()
    days, exponent = official_tgif(holidays)
    shutil.copyfile("tgif.html.template", "tgif.html")
    replace("tgif.html", "#DAYS#", str(days))
    replace("tgif.html", "#EXPONENT#", str(exponent))
    s3_client.upload("tgif.html")

    exponent_str = exponent_table.get(exponent, "^{}".format(exponent))
    slack_client.chat_postMessage(
        channel="general",
        text="TGIF{}-{}".format(exponent_str, days)
    )

schedule.every().day.at("07:00").do(job, None)

#job()
while True:
    schedule.run_pending()
    time.sleep(60*60) # check schedule every hour

