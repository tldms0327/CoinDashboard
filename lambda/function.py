import boto3
from requests_aws4auth import AWS4Auth
import datetime
import requests
import json


region = "ap-northeast-2"
service = "es"
creds = boto3.Session().get_credentials()
awsauth = AWS4Auth(creds.access_key, creds.secret_key, region, service)

client = boto3.client("s3", "ap-northeast-2")
BUCKET_NAME = "coinboard"


def sendData(data, index):
    host = "https://search-testing1-b4cxlyyuyp3ofvneweziyxgnia.ap-northeast-2.es.amazonaws.com"
    t = "_doc"
    headers = {"Content-Type": "application/json"}
    url = host + "/" + index + "/" + t
    # index 마다 데이터가 다르니 여기에 서 변형해서 전송까지
    data.pop("index", None)
    now = datetime.datetime.now()
    t = now.strftime("%Y-%m-%d %H:%M:%S")
    data["datetime"] = t
    r = requests.post(url, auth=awsauth, json=data, headers=headers)


def handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        obj = client.get_object(bucket, key)
        body = obj["Body"].read()
        lines = body.splitlines()

        if len(lines) != 0:
            for line in lines:
                line = json.loads(line.decode())
                sendData(line, line["index"].lower())
