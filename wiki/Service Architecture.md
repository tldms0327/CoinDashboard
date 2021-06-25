# 데이터 흐름

![1](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/456ecfe6-81eb-470d-920d-e181a636038a/_2021-06-25__8.52.44.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210625%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210625T134431Z&X-Amz-Expires=86400&X-Amz-Signature=d9f372af098d753c91d72b1b8b77b98d802b9bd88c17aa02340b1a487568cbff&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22_2021-06-25__8.52.44.png%22)

### Data Source

- Binance API - 1m Kline Chart

### Kinesis Producer

- 총 331개의 코인
- 한 컨테이너 당 20개의 소켓을 열어, 20개 코인에 대한 정보를 실시간 조회
- 수집된 데이터는 AWS kinesis DataStream으로 실시간 전송
- 331/20 개의 도커 컨테이너를 ECS 클러스터에 배포(현재 100개의 코인 트래킹, scale in/out 용이)

### Kinesis FireHose & Glue

- 실시간으로 수집되는 데이터에 대한 스키마를 Glue 정의
- 1분에 한번씩 새로운 데이터를 elasticsearch에 전송, S3에는 parquet 형식으로 저장

### EMR

![2](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/813387a9-f933-4faa-853f-f3d4967a1811/_2021-06-25__10.19.31.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20210625%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20210625T134448Z&X-Amz-Expires=86400&X-Amz-Signature=e7e37fa3b7a0188a846db5f3dfc65023ba3633fb9d448ddcee8865e0ca89b059&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22_2021-06-25__10.19.31.png%22)

- DataStreamReader 객체를 이용하여 S3에 전송되는 parquet를 실시간으로 읽고 계산
- 총 8개의 지표: 장/단기 이동평균, Bollinger Band, Stochastic, CCI, 1mRate, 1hRate, RSI
- Streaming 처리를 통해 실시간으로 지표를 업데이트하여 json형식으로 S3에 전송

### Lambda Trigger

- EMR에서 계산된 지표가 S3에 업데이트 될 때마다 lambda함수를 trigger하여 elasticsearch로 지표 전송

### Kibana

- Producer에서 가져온 raw data와 지표를 통한 시각화