# Kinesis - Data Stream, Firehose

1개의 **Data Stream**과 2개의 **Data Firehose**로 구성

1. **Data Stream**
- **Data Source**: **Binance API**로부터 데이터 생성, **Data Firehose**와 연결

    - **Websocket API**를 활용하였고, 여러 코인의 데이터를 받아오기 위하여 다수의 스레드를 활용하였다.

```java
twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
twm.start()
twm.start_multiplex_socket(callback=handle_socket_message, streams=streams)
twm.join()
```

![1](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/2f5b0b37-3e55-4b7a-a161-65d278d525c3/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210626%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210626T072517Z&X-Amz-Expires=86400&X-Amz-Signature=d93fd0f23e95bcd4c3ef79e36ab9c0a61363fdb698668579477e13db8795f50e&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)

2.  **Data Firehose**

Binance API로부터 생성된 데이터가 들어있는 Data Stream으로부터 데이터를 끌어와 AWS내의 다른 도메인에 제공한다.

**(1)** 실시간 정보를 **Elasticsearch**로 forwarding하여 분석 및 시각화를 위한 **Data Firehose**

**(2)** **EMR**에서 각종 지표를 계산하기 위하여 **S3**로 데이터를 변환, 전달하는 **Data Firehose** - 데이터 타입의 변환을 위해 **AWS Glue**를 활용하였다.

![2](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/9e5ad6b9-d9b2-47aa-be5d-509c3526fbae/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210626%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210626T072904Z&X-Amz-Expires=86400&X-Amz-Signature=75f58afa11246863997a370778a7f5e6f2a4da954e360c6ff4544c9b37b37eeb&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)

- **AWS Glue:** 데이터 전달 과정에서의 타입 변환에 이용
- 데이터 입출력 형식, 스키마 지정

![3](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/c6afaba5-0321-4787-96ac-8d65b2c84bd5/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210626%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210626T072938Z&X-Amz-Expires=86400&X-Amz-Signature=f971fdee419d6fa8e21628e59e55cac8645f3ae2a962a0732e62cf9b3f546c36&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)

![4](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/179b4601-24a4-4822-83a7-a44f65250e4a/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210626%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210626T072953Z&X-Amz-Expires=86400&X-Amz-Signature=cc6a3a57a499cc1e0a4bb75a2f5cd5a234b9d34e82176dc87617be257d8e94be&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22Untitled.png%22)