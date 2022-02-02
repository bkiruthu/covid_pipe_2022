import requests
import boto3
import time
import json
import datetime
import pytz

year = yesterday.strftime("%Y")
month = yesterday.strftime("%m")
day = yesterday.strftime("%d")

def rapid_api():
    path = "https://api.covid19api.com/live/country/usa/status/confirmed/date/"
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)

    url = path + str(yesterday)

    payload = {}
    headers = {}
    
    response = requests.request("GET", url, headers=headers, data=payload)
    rawdata=response.json
    return rawdata


# handler for lambda
def covid(event, context):
    data_output=rapid_api()
    tz = pytz.timezone("US/Eastern")
    timestamp = datetime.datetime.now(tz).strftime("%m_%d_%y_%H%M")
    file_name =f"covid-{timestamp}.json"
    print(file_name)
    bucket_name = f"cdc-ohio-covid/{year}/{month}/{day}"
    save_file_to_s3(bucket_name, file_name, data_output)
    timestamp = None

# save to a bucket
def save_file_to_s3(bucket, file_name, data_output):
   s3 = boto3.resource('s3')
   obj = s3.Object(bucket, file_name)
   tmp_file_path = "/tmp/nyrawdata.json"
   with open(tmp_file_path, "w") as file:
       file.write(str(data_output))
    
   s3.Bucket(bucket).upload_file(tmp_file_path, file_name)
   print('file added to s3')







