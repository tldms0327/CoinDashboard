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

![Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled.png](Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled.png)

2.  **Data Firehose**

Binance API로부터 생성된 데이터가 들어있는 Data Stream으로부터 데이터를 끌어와 AWS내의 다른 도메인에 제공한다.

**(1)** 실시간 정보를 **Elasticsearch**로 forwarding하여 분석 및 시각화를 위한 **Data Firehose**

**(2)** **EMR**에서 각종 지표를 계산하기 위하여 **S3**로 데이터를 변환, 전달하는 **Data Firehose** - 데이터 타입의 변환을 위해 **AWS Glue**를 활용하였다.

![Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled%201.png](Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled%201.png)

- **AWS Glue:** 데이터 전달 과정에서의 타입 변환에 이용

    - 데이터 입출력 형식, 스키마 지정

![Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled%202.png](Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled%202.png)

![Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled%203.png](Kinesis%20-%20Data%20Stream,%20Firehose%20594b648d0e804c4f94d3d8ddfecf2b53/Untitled%203.png)