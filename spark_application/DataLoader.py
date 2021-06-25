from pyspark.sql import SQLContext, SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime, timedelta

from IndicatorCalculator import IndicatorCalculator


class DataLoader:
    def __init__(self, spark):
        self.spark = spark

    def getIndicators(self, batch, epoch_id):
        calculate = IndicatorCalculator(batch, epoch_id)
        calculate.MvaLong()
        calculate.MvaShort_Cci()
        calculate.Bollinger()
        calculate.Stochastic()
        calculate.RSI()

    def streaming_calculation(self):
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

        writerDF = self.spark.sql(time_convert_sql).writeStream.foreachBatch(self.getIndicators).start()
        writerDF.awaitTermination()
