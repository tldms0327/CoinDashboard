# Data Stream Analysis with EMR

EMR에서 스트림 데이터를 다루기 위해 시도했던 방법들을 정리한 글입니다.

```
spec:
	spark v2.4.7
	zeppelin v0.9.0
	scala v2.1.1
	java v1.8.0
	python v3.7.9
```

### kinesis와 emr을 직접 연결하기(실패)

1. **spark**에서 **kinesis stream**을 사용하기 위한 준비사항

    spark application에 필요한 jar 파일을 maven에서 다운로드하고, dependency를 설정했다.

    [](https://mvnrepository.com)

    ```bash
    #amazon-kinesis-client-1.8.0.jar
    #spark-sql-kinesis-asl_2.11-2.4.2-atlassian-1.jar
    #spark-streaming-kinesis-asl_2.11-2.4.7.jar

    $ sudo cp {jars} /usr/lib/spark/jars
    # or
    $ spark-submit --jars {jars}
    ```

    제플린 인터프리터에서도 사용할 수 있게 설정해준다.

2. **zeppelin**에서 **kinesis stream**에 연결하기

    ```python
    from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
    from pyspark.streaming import StreamingContext
    from pyspark import StorageLevel
    from pyspark import SparkContext

    spark_session = SparkSession.builder.getOrCreate()
    sc = spark_session.sparkContext
    k = StreamingContext(sc, 10)
    # <pyspark.streaming.context.StreamingContext object at 0x7fc76ef42510>

    appName = "Test_Consumer" # dynamo db 테이블 이름, 없으면 자동생성됨!checkpoint저장
    streamName = "coinBoard"
    endpoint_url = "https://kinesis.ap-northeast-2.amazonaws.com"
    regionName = "ap-northeast-2"

    kinesis = KinesisUtils.createStream(ssc, appName, streamName, endpoint_url, regionName, InitialPositionInStream.TRIM_HORIZON, 1)

    kinesis.pprint([0]) # -> 아무것도 안나옴 ㅠㅠ
    ```

    위와 같이 실행하면 `StreamingContext`객체가 생성된다. 받아온 데이터에 간단한 연산을 하여 데이터를 확인하고자 했다.

    ```python
    from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
    from pyspark.streaming import StreamingContext
    from pyspark import StorageLevel
    from pyspark import SparkContext

    appName = "test" # dynamo db 테이블 이름, 없으면 자동생성됨!
    streamName = "coinBoard"
    endpoint_url = "[https://kinesis.ap-northeast-2.amazonaws.com](https://kinesis.ap-northeast-2.amazonaws.com/)"
    regionName = "ap-northeast-2"

    def process_stream(record, spark):
    	if not record.isEmpty():
    		df = spark.createDataFrame(record)
    		df.show()

    def main():
    	spark_session = SparkSession.builder.getOrCreate()
    	sc = spark_session.sparkContext
    	ssc = StreamingContext(sc, 5)
    	kinesis = KinesisUtils.createStream(ssc, appName, streamName, endpoint_url, regionName, InitialPositionInStream.TRIM_HORIZON, 1)
    	
    	kinesis.foreachRDD(lambda rdd: process_stream(rdd, spark))
    		ssc.start()
    	ssc.awaitTermination()

    main()
    ```

    ```python
    Py4JJavaError: An error occurred while calling o232.awaitTermination.
    : java.net.ConnectException: Connection refused (Connection refused)
    	at java.net.PlainSocketImpl.socketConnect(Native Method)
    	at java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:350)
    	at java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:206)
    	at java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:188)
    	at java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
    	at java.net.Socket.connect(Socket.java:607)
    	at java.net.Socket.connect(Socket.java:556)
    	at java.net.Socket.<init>(Socket.java:452)
    	at java.net.Socket.<init>(Socket.java:262)
    	at javax.net.DefaultSocketFactory.createSocket(SocketFactory.java:277)
    	at py4j.CallbackConnection.start(CallbackConnection.java:226)
    	at py4j.CallbackClient.getConnection(CallbackClient.java:238)
    	at py4j.CallbackClient.getConnectionLock(CallbackClient.java:250)
    	at py4j.CallbackClient.sendCommand(CallbackClient.java:377)
    	at py4j.CallbackClient.sendCommand(CallbackClient.java:356)
    	at py4j.reflection.PythonProxyHandler.invoke(PythonProxyHandler.java:106)
    	at com.sun.proxy.$Proxy62.call(Unknown Source)
    	at org.apache.spark.streaming.api.python.TransformFunction.callPythonTransformFunction(PythonDStream.scala:92)
    	at org.apache.spark.streaming.api.python.TransformFunction.apply(PythonDStream.scala:78)
    	at org.apache.spark.streaming.api.python.PythonTransformedDStream.compute(PythonDStream.scala:246)
    	at org.apache.spark.streaming.dstream.DStream$$anonfun$getOrCompute$1$$anonfun$1$$anonfun$apply$7.apply(DStream.scala:342)
    	at org.apache.spark.streaming.dstream.DStream$$anonfun$getOrCompute$1$$anonfun$1$$anonfun$apply$7.apply(DStream.scala:342)
    	at scala.util.DynamicVariable.withValue(DynamicVariable.scala:58)
    	at org.apache.spark.streaming.dstream.DStream$$anonfun$getOrCompute$1$$anonfun$1.apply(DStream.scala:341)
    	at org.apache.spark.streaming.dstream.DStream$$anonfun$getOrCompute$1$$anonfun$1.apply(DStream.scala:341)
    	at org.apache.spark.streaming.dstream.DStream.createRDDWithLocalProperties(DStream.scala:416)
    	at org.apache.spark.streaming.dstream.DStream$$anonfun$getOrCompute$1.apply(DStream.scala:336)
    	at org.apache.spark.streaming.dstream.DStream$$anonfun$getOrCompute$1.apply(DStream.scala:334)
    	at scala.Option.orElse(Option.scala:289)
    	at org.apache.spark.streaming.dstream.DStream.getOrCompute(DStream.scala:331)
    	at org.apache.spark.streaming.dstream.ForEachDStream.generateJob(ForEachDStream.scala:48)
    	at org.apache.spark.streaming.DStreamGraph$$anonfun$1.apply(DStreamGraph.scala:122)
    	at org.apache.spark.streaming.DStreamGraph$$anonfun$1.apply(DStreamGraph.scala:121)
    	at scala.collection.TraversableLike$$anonfun$flatMap$1.apply(TraversableLike.scala:241)
    	at scala.collection.TraversableLike$$anonfun$flatMap$1.apply(TraversableLike.scala:241)
    	at scala.collection.mutable.ResizableArray$class.foreach(ResizableArray.scala:59)
    	at scala.collection.mutable.ArrayBuffer.foreach(ArrayBuffer.scala:48)
    	at scala.collection.TraversableLike$class.flatMap(TraversableLike.scala:241)
    	at scala.collection.AbstractTraversable.flatMap(Traversable.scala:104)
    	at org.apache.spark.streaming.DStreamGraph.generateJobs(DStreamGraph.scala:121)
    	at org.apache.spark.streaming.scheduler.JobGenerator$$anonfun$3.apply(JobGenerator.scala:249)
    	at org.apache.spark.streaming.scheduler.JobGenerator$$anonfun$3.apply(JobGenerator.scala:247)
    	at scala.util.Try$.apply(Try.scala:192)
    	at org.apache.spark.streaming.scheduler.JobGenerator.generateJobs(JobGenerator.scala:247)
    	at org.apache.spark.streaming.scheduler.JobGenerator.org$apache$spark$streaming$scheduler$JobGenerator$$processEvent(JobGenerator.scala:183)
    	at org.apache.spark.streaming.scheduler.JobGenerator$$anon$1.onReceive(JobGenerator.scala:89)
    	at org.apache.spark.streaming.scheduler.JobGenerator$$anon$1.onReceive(JobGenerator.scala:88)
    	at org.apache.spark.util.EventLoop$$anon$1.run(EventLoop.scala:49)

    (<class 'py4j.protocol.Py4JJavaError'>, Py4JJavaError('An error occurred while calling o232.awaitTermination.\n', JavaObject id=o241), <traceback object at 0x7f5036c11370>)
    ```

    위와 같이 Connection refused 되며 데이터를 받아오지 못했다... 보안 설정도 보고, jar 파일 버전도 바꿔가며 여러가지 시도를 해봤지만 안 돼서 다른 방법을 모색했다. 시간이 없어서 ㅠ.ㅠ

[Spark Streaming + Kinesis Integration](https://spark.apache.org/docs/2.4.7/streaming-kinesis-integration.html)

### kinesis → s3 → emr로 연결하기(성공)

1. **kinesis firehose**, **Glue**를 이용하여 producer에서 보낸 데이터에 schema를 씌워 **parquet**로 **S3**에 전송했다.
2. emr에서 S3를 **스트림 형식**으로 읽는다.

```python
from pyspark.sql.functions import *
from pyspark.sql import Row
from pyspark.sql.types import *

df_schema=spark.read.parquet("s3://coinboard2/*.parquet")
user_schema = df_schema.schema
parquet_sdf = spark.readStream.schema(user_schema).parquet("s3://coinboard2/*")
# count = parquet_sdf.groupBy('symbol').count()
# count.writeStream.outputMode("complete").format("console").start()

parquet_sdf.writeStream.queryName("test").format("memory").start()
```

처음 시도했을때, zeppelin user가 admin group에 추가되지 않아 /mnt/tmp 폴더에 대한 권한이 없어 실행되지 않았다. spark-shell에서 실행했을때 문제없이 작동되는 것을 확인했다. 우리는 제플린에서 지표를 만들고 디버깅해야 하므로, zeppelin 유저를 hadoopadmin 그룹에 추가했다. 

```bash
$ group zeppelin # zeppelin : zeppelin
$ sudo gpasswd -a zeppelin hdfsadmingroup
$ group zeppelin # zeppelin : zeppelin hdfsadmingroup
```

`writeStream` 할 때 `queryName`을 설정하면 테이블로서 접근 가능하다.

![Data%20Stream%20Analysis%20with%20EMR%20ec4d7544f5e8495ea49c4792ed75ff83/_2021-06-24__2.37.53.png](Data%20Stream%20Analysis%20with%20EMR%20ec4d7544f5e8495ea49c4792ed75ff83/_2021-06-24__2.37.53.png)

**성공..!** 🤩