# Lambda Trigger

1. **AWS Lambda** 함수 생성

![1](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/6c994bc5-e67a-473b-a64d-c410832dda85/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210626%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210626T071654Z&X-Amz-Expires=86400&X-Amz-Signature=fa8eaf3b10dcb95f3432d4114eb13c710ee3f7d124818544a908d50ae80a88f0&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)

2.  트리거 지정 - **S3**의 지정된 버킷에서 `indicator/*.json` 파일 신규 생성 시 지정된 코드 실행

![2](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/cc71144f-8084-4962-8b23-f3becf745a0c/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210626%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210626T071910Z&X-Amz-Expires=86400&X-Amz-Signature=229553c45d9a07c56a83bf5c08e65e24710bc7341c52be17d76cd6cc28c383aa&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)

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

