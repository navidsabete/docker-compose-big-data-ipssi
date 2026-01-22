import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, count
from pyspark.sql.types import StructType, StructField, DoubleType, BooleanType, StringType, TimestampType


SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")


def main():
    spark = SparkSession.builder \
        .appName("WeatherAggregation") \
        .master(SPARK_MASTER_URL) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0" ) \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")

    schema = StructType([ 
        StructField("temperature", DoubleType(), True), 
        StructField("windspeed", DoubleType(), True), 
        StructField("temp_f", DoubleType(), True), 
        StructField("high_wind_alert", BooleanType(), True), 
        StructField("time", StringType(), True) ])
    
    raw_df = spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", KAFKA_BROKER) \
            .option("subscribe", "weather_transformed") \
            .option("startingOffsets", "earliest") \
            .load()
    
    json_df = raw_df.selectExpr("CAST(value AS STRING) as json") 
    parsed = json_df.select(from_json(col("json"), schema).alias("data")).select("data.*")
    parsed = parsed.withColumn("event_time", col("time").cast(TimestampType()))

    agg = parsed.groupBy(
        window(col("event_time"), "1 minute")
    ).agg(
        avg("temperature").alias("avg_temp_c"),
        count(col("high_wind_alert")).alias("alert_count")
        )
    agg.show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()