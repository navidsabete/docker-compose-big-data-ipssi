import os
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, count
from pyspark.sql.types import StructType, StructField, DoubleType, BooleanType, StringType, TimestampType
from hdfs import InsecureClient
from hdfs.util import HdfsError
from datetime import datetime
import json
import csv
import io
import traceback

SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")

# Connexion HDFS
HDFS_URL = "http://namenode:9870"  # URL de ton NameNode

HDFS_USER = "root"              # utilisateur HDFS
#HDFS_USER = "jovyan"
HDFS_DIR = f"/user/jovyan/weather_agg"

hdfs_client = InsecureClient(HDFS_URL, user=HDFS_USER)


def init_spark():
    spark = SparkSession.builder \
        .appName("WeatherAggregation") \
        .getOrCreate()
    return spark

def kafka_read(spark):
    schema = StructType([ 
        StructField("temperature", DoubleType(), True), 
        StructField("windspeed", DoubleType(), True), 
        StructField("temp_f", DoubleType(), True), 
        StructField("high_wind_alert", BooleanType(), True), 
        StructField("time", StringType(), True) ])
    raw_df = spark.read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "kafka:9092") \
            .option("subscribe", "weather_transformed") \
            .option("startingOffsets", "earliest") \
            .load()
    json_df = raw_df.selectExpr("CAST(value AS STRING) as json")
    parsed = json_df.select(from_json(col("json"), schema).alias("data")).select("data.*")
    parsed = parsed.withColumn("event_time", col("time").cast(TimestampType()))
    return parsed
    

def main():
    print("spark master url: ",  SPARK_MASTER_URL)
    print("kafka broker : ", KAFKA_BROKER)
    spark = init_spark()
    print("✅ Spark session started !")
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    print("✅ Spark session started LOG WARN!")

    parsed_data = kafka_read(spark)
    agg = parsed_data.groupBy(
        window(col("event_time"), "1 minute")
    ).agg(
        avg("temperature").alias("avg_temp_c"),
        count(col("high_wind_alert")).alias("alert_count")
        )
    results = agg.collect()
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # En-têtes CSV
    writer.writerow([
        "window_start",
        "window_end",
        "avg_temp_c",
        "alert_count"
    ])

    # Lignes
    for row in results:
        writer.writerow([
            row["window"].start,
            row["window"].end,
            row["avg_temp_c"],
            row["alert_count"]
        ])

    print("📦 VERIFICATION DOSSIER")
    try:
        hdfs_client.status(HDFS_DIR)
        print(f"✅ HDFS directory exists: {HDFS_DIR}")
    except HdfsError:
        print(f"📁 Creating HDFS directory: {HDFS_DIR}")
    hdfs_client.makedirs(HDFS_DIR)

    print("📂 HDFS root content:", hdfs_client.list("/user/jovyan"))

    # Nom de fichier horodaté
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"weather_agg_{ts}.csv"
    hdfs_path = f"{HDFS_DIR}/{filename}"

    # Écriture HDFS
    with hdfs_client.write(hdfs_path, overwrite=False, encoding="utf-8") as writer:
        writer.write(buffer.getvalue())

    print("✅ CSV aggregation saved to HDFS:", hdfs_path)
    
    #agg.show(truncate=False)

    
if __name__ == "__main__":
    main()

#    spark.stop()


