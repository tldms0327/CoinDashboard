# 데이터 흐름

![%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%92%E1%85%B3%E1%84%85%E1%85%B3%E1%86%B7%20fb213a37147e4fc6b04795ef1dda2f0d/_2021-06-25__8.52.44.png](%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%92%E1%85%B3%E1%84%85%E1%85%B3%E1%86%B7%20fb213a37147e4fc6b04795ef1dda2f0d/_2021-06-25__8.52.44.png)

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

![%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%92%E1%85%B3%E1%84%85%E1%85%B3%E1%86%B7%20fb213a37147e4fc6b04795ef1dda2f0d/_2021-06-25__10.19.31.png](%E1%84%83%E1%85%A6%E1%84%8B%E1%85%B5%E1%84%90%E1%85%A5%20%E1%84%92%E1%85%B3%E1%84%85%E1%85%B3%E1%86%B7%20fb213a37147e4fc6b04795ef1dda2f0d/_2021-06-25__10.19.31.png)

- DataStreamReader 객체를 이용하여 S3에 전송되는 parquet를 실시간으로 읽고 계산
- 총 8개의 지표: 장/단기 이동평균, Bollinger Band, Stochastic, CCI, 1mRate, 1hRate, RSI
- Streaming 처리를 통해 실시간으로 지표를 업데이트하여 json형식으로 S3에 전송

### Lambda Trigger

- EMR에서 계산된 지표가 S3에 업데이트 될 때마다 lambda함수를 trigger하여 elasticsearch로 지표 전송

### Kibana

- Producer에서 가져온 raw data와 지표를 통한 시각화