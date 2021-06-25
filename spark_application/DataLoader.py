from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext, SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime, timedelta
from pyspark.sql.window import Window

import time


class DataLoader():
    def __init__(self, spark):
        self.spark = spark

    def getIndicators(self, batch, epoch_id):
        # MVA
        mva_long = batch.groupby('symbol').agg(avg('close_price').alias('mva_long')).withColumn("index",
                                                                                                lit("mva_long"))
        mva_long.write.mode('append').json("s3://coinboard/indicator/mva_long")
        print("=== mva_long DONE ===")
        mva_short = batch.filter(batch.opentime > datetime.now() - timedelta(hours=1)). \
            groupby('symbol').agg(avg('close_price').alias('mva_short')).withColumn("index", lit("mva_short"))

        # CCI
        df3 = batch.sort(asc('opentime')).groupby('symbol'). \
            agg(min('close_price').alias('min'), max('close_price').alias('max'), last('close_price').alias('last')). \
            withColumnRenamed("symbol", "symbol_b")
        join_exp = [mva_short.symbol == df3.symbol_b]
        cci = df3.withColumn('sum', (col("max") + col("min") + col("last")) / 3).join(mva_short, join_exp, 'inner'). \
            withColumn('cci', (col('sum') * col('mva_short')) / ((col('sum') - col('mva_short')) * 0.015)).na.fill(0). \
            withColumn("index", lit("cci")).select('symbol', 'cci', "index")
        cci.write.mode('append').json("s3://coinboard/indicator/cci")
        print("=== cci DONE ===")

        mva_short.write.mode('append').json("s3://coinboard/indicator/mva_short")
        print("=== mva_short DONE ===")

        # Bollinger Band
        bollinger_band = batch.groupBy("symbol").agg(avg("close_price").alias("avg"),
                                                     stddev_pop("close_price").alias("stddev")) \
            .withColumn("Upper", col("avg") + 2 * col("stddev")).withColumn("Lower", col("avg") - 2 * col("stddev")) \
            .withColumn("index", lit("bollinger"))
        bollinger_band.write.mode('append').json("s3://coinboard/indicator/bollinger")
        print("=== bollinger DONE ===")

        # Stochastic
        df1 = batch.groupBy("symbol").agg(max("opentime").alias("latest_time"), max("close_price").alias("max_price"),
                                          min("close_price").alias("min_price")) \
            .withColumn("diff", col("max_price") - col("min_price"))
        df2 = batch.withColumnRenamed("opentime", "opentime_B") \
            .withColumnRenamed("symbol", "symbol_B") \
            .select("symbol_B", "opentime_B", "close_price")
        joinType = "inner"
        joinExpression = [df1.symbol == df2.symbol_B, df1.latest_time == df2.opentime_B]
        stochastic = df1.join(df2, joinExpression, joinType) \
            .withColumn("Stochastic",
                        (col("close_price") - col("min_price")) / col(
                            "diff") * 100) \
            .withColumn("index", lit("stochastic")) \
            .select("symbol", "Stochastic", "index")
        stochastic.write.mode('append').json("s3://coinboard/indicator/stochastic")
        print("=== Stochastic DONE ===")

        # order by opentime, partition by symbol and add row num
        partitioned_batch = batch.select("opentime", "symbol", "close_price",
                                         row_number().over(
                                             Window.partitionBy("symbol").orderBy(col("opentime").desc())).alias(
                                             "row_num"))
        # lag
        Windowspec = Window.orderBy("symbol")
        df_prev = partitioned_batch.withColumn('prev_price', lag(batch['close_price'], 1).over(Windowspec))
        # calculate 1m rate
        df_prev_1m = df_prev.withColumn('1mRate',
                                        (df_prev['prev_price'] - df_prev['close_price']) / df_prev['close_price'])
        # filter 1m rate
        df_1m = df_prev_1m.filter(df_prev_1m.row_num == 2).withColumn("index", lit("1mRate")).select("symbol", "1mRate",
                                                                                                     "index")
        df_1m.write.mode('append').json("s3://coinboard/indicator/1mRate")
        print("=== 1mRate DONE === ")

        # get current and 1h prev price
        df3 = partitioned_batch.filter((partitioned_batch.row_num == 1) | (partitioned_batch.row_num == 60))
        # lag
        Windowspec = Window.orderBy("symbol")
        df_prev = df3.withColumn('prev_price', lag(df3['close_price'], 1).over(Windowspec))
        # calculate 1h rate
        df_prev_1h = df_prev.withColumn('1hRate',
                                        (df_prev['prev_price'] - df_prev['close_price']) / df_prev['close_price'])
        # filter 1h rate
        df_1h = df_prev_1h.filter(df_prev_1h.row_num == 60). \
            withColumn("index", lit("1hRate")).select("symbol", "1hRate", "index")
        df_1h.write.mode('append').json("s3://coinboard/indicator/1hRate")
        print("=== 1hRate DONE === ")

        # get 4h data
        df4 = partitioned_batch.filter(partitioned_batch.row_num <= 240)
        # lag
        Windowspec = Window.orderBy("symbol")
        df_prev = df3.withColumn('prev_price', lag(df4['close_price'], 1).over(Windowspec))
        # calculate increase rate
        df_rate = df_prev.withColumn('rate', (df_prev['prev_price'] - df_prev['close_price']) / df_prev['close_price'])
        # divide increased/decreased
        df_U = df_rate.filter(df_rate.rate > 0).select("symbol", "rate")
        df_D = df_rate.filter(df_rate.rate < 0).select("symbol", "rate")
        # average
        df_AU = df_U.groupby('symbol').agg(avg('rate').alias('AU'))
        df_AD = df_D.groupby('symbol').agg(avg('rate').alias('AD'))
        # join 2 dataframes and calculate rsi
        joinType = "inner"
        joinExpression = [df_AU.symbol == df_AD.symbol]
        df_rsi = df_AU.join(df_AD, joinExpression, joinType) \
            .withColumn("rsi", col('AU') / (col('AU') + col('AD'))) \
            .withColumn("index", lit("rsi")).select(df_AU.symbol, "rsi", "index")
        df_rsi.write.mode('append').json("s3://coinboard/indicator/rsi")

        print("=== RSI DONE === ")

    def test(self):
        print("Application is starting...")
        df_schema = self.spark.read.parquet("s3://coinboard2/*.parquet")
        user_schema = df_schema.schema

        time_convert_sql = """
            SELECT 
            symbol, 
            opentime, 
            close_price, 
            high_price, low_price,
            num_trades, quote_asset_volume  
            FROM coin
            WHERE opentime + INTERVAL 4 hours >= now()"""

        streamingDF = self.spark.readStream.schema(user_schema).parquet("s3://coinboard2/*")
        streamingDF.registerTempTable("coin")
        print("===stage: registerTemptable DONE===")

        test = self.spark.sql(time_convert_sql).writeStream.foreachBatch(self.getIndicators).start()
        test.awaitTermination()
