import boto3
from aws4auth.requests_aws4auth import AWS4Auth
from botocore.vendored import requests
import json
from time import time

region = "ap-northeast-2"
service = "es"
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


def lambda_handler(event, context):
    client = boto3.client("s3", "ap-northeast-2")

    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

    obj = client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()
    lines = body.splitlines()

    if len(lines) != 0:
        for line in lines:
            line = json.loads(line.decode())
            if "index" in line:
                sendData(line, line["index"])

    return {
        'status': 200
    }


def sendData(data, index):
    host = "https://search-testing1-b4cxlyyuyp3ofvneweziyxgnia.ap-northeast-2.es.amazonaws.com"
    t = "_doc"
    headers = {"Content-Type": "application/json"}
    url = host + "/" + index + "/" + t
    # index 마다 데이터가 다르니 여기에 서 변형해서 전송까지
    data.pop("index", None)
    unix = int(time()) * 1000
    data["datetime"] = unix

    r = requests.post(url, json=data, headers=headers, auth=awsauth)
    print("status: ", r.text)
