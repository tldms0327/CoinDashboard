# CoinPrediction

### 21-1 YBIGTA Conference
팀원: 김성하(18기), 노연수(17기), 안범진(18기), 이동주(17기), 이시은(16기), 안지훈(17기), 주우진(18기)

프로젝트 기간: 6/20 ~ 6/26

## 프로젝트 개요

바야흐로 대 코인시대! 정보가 난무하는 코인 시장에서 당신의 성투(성공적인 투자)를 위한 코인 정보 대시보드입니다.

저희는 Binance API로부터 코인 가격 데이터를 가져와 실시간 가격 정보 뿐만 아니라 볼린저 밴드, 1시간/1분 변동률, CCI지표, Stochastic지표, RSI지표,단순이동평균을 한눈에 보여주는 대시보드를 제작하였습니다.

이 과정에서 AWS 클라우드 컴퓨팅 서비스, Python, ElasticSearch,Spark를 활용하였습니다.

## 프로젝트 아키텍쳐

![image](https://user-images.githubusercontent.com/61309514/125166031-a60b3200-e1d4-11eb-82e5-bda2c7931c84.png)

### 1. Binance API & Producer

Binance API가 제공해주는 코인 데이터를 Producer가 가져온 후 이를 Kinesis DataStream으로 전송해 줍니다.

### 2. AWS Kinesis & Glue

Kinesis DataStream에 저장되어 있는 데이터 레코드를 Kinesis Firehose를 이용해 S3, ElasticSearch에 보내줍니다. S3 객체로 저장된 데이터는 AWS Glue를 통해 parquet형식으로 저장됩니다.

### 3. Spark on AWS EMR & S3

S3에 데이터가 저장되는 즉시 AWS EMR 위에서 작동하는 Spark Streaming이 해당 S3 객체를 스트리밍 객체로 읽어옵니다. 그리고 Spark SQL을 이용해 각종 지표를 계산해 냅니다. 이렇게 계산된 지표는 다시 S3에 Json형식으로 저장됩니다.

### 4. Lamda

앞서 S3에 저장된 Json 형식의 파일은 AWS Lambda에 의해 저장되는 즉시 ElasticSearch로 전송됩니다.

### 5. ElasticSearch & Kibana

ElasticSearch에 저장된 실시간 코인 데이터, 지표 데이터는 Kibana를 통해 시각화되어 대시보드에 나타납니다.

<br>

## Repository

- api : bithumb api analysis
- binance_producer : binance api에서 kinesis datastream으로의 데이터 전송을 위한 producer 코드 (+Dockerfile)
- data_schema : AWS glue와 elasticsearch에 사용된 데이터 스키마
- lambda : lambda function 코드
- spark_application : EMR에서의 지표 계산을 위한 spark application
- wiki : 기술 사용법에 대한 정리

<br>

## 발표 영상

21-1 YBIGTA Conference에서 발표했던 영상은 [Youtube](https://www.youtube.com/watch?v=Cy7RHdDHDjM)에 업로드되어 있습니다. 

<br>

## 구글 드라이브 링크 (프로젝트 시연,  발표자료)

21-1 YBIGTA Conference에 사용되었던 발표자료는 [구글드라이브](https://drive.google.com/file/d/14YkgRYJirfiCuKU5kBZFuMeOvTPZCVxP/view?usp=sharing) 에 업로드되어 있습니다. 
