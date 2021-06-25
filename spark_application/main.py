from DataLoader import DataLoader
from pyspark.sql import SparkSession

if __name__ == "__main__":
    # init spark session
    spark = SparkSession.builder.appName("indicators-calculator").getOrCreate()

    data_loader = DataLoader(spark)
    data_loader.streaming_calculation()
