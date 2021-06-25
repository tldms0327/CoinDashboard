# Lambda Trigger

1. **AWS Lambda** 함수 생성

![Lambda%20Trigger%20c68d2ef9d7124e68aff7d8bf891401a3/Untitled.png](Lambda%20Trigger%20c68d2ef9d7124e68aff7d8bf891401a3/Untitled.png)

2.  트리거 지정 - **S3**의 지정된 버킷에서 `indicator/*.json` 파일 신규 생성 시 지정된 코드 실행

![Lambda%20Trigger%20c68d2ef9d7124e68aff7d8bf891401a3/Untitled%201.png](Lambda%20Trigger%20c68d2ef9d7124e68aff7d8bf891401a3/Untitled%201.png)

3.  **S3**에 생성된 파일의 내용을 **Elasticsearch**에 전달

```python
def sendData(data, index):
host = "[https://search-testing1-b4cxlyyuyp3ofvneweziyxgnia.ap-northeast-2.es.amazonaws.com](https://search-testing1-b4cxlyyuyp3ofvneweziyxgnia.ap-northeast-2.es.amazonaws.com/)"
t = "_doc"
headers = {"Content-Type": "application/json"}
url = host + "/" + index + "/" + t
# index 마다 데이터가 다르니 여기에 서 변형해서 전송까지
data.pop("index", None)
unix = int(time()) * 1000
data["datetime"] = unix

r = requests.post(url, json=data, headers=headers,auth=awsauth)
print("status: ", r.text)
```

생성된 **JSON** 파일 예시:

```json
{"symbol":"WTCBTC",
"avg":622.8000000000001,
"stddev":0.6531972647422598,
"Upper":624.1063945294845,
"Lower":621.4936054705156,
"index":"bollinger"}
```