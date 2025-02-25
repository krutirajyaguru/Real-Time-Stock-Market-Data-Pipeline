from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType, TimestampType
import time

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaStockStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

# Define Kafka Source
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "stock-topic-1"

# Define Schema
schema = StructType() \
    .add("symbol", StringType()) \
    .add("price", FloatType()) \
    .add("high", FloatType()) \
    .add("low", FloatType()) \
    .add("open", FloatType()) \
    .add("timestamp", StringType())

# Read from Kafka
# failOnDataLoss: allows Spark job to continue running even if some Kafka messages were deleted.
# startingOffsets: Avoids processing deleted offsets # .option("startingOffsets", "latest") \
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("failOnDataLoss", "false") \
    .load()

# Parse JSON
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")


query = parsed_df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "/Users/kafka_airflow_spark_venv/Parquet_Data/parquet_checkpoint/") \
    .option("path", "/Users/kafka_airflow_spark_venv/Parquet_Data/parquet_table/") \
    .outputMode("append") \
    .start()

'''# Write to Delta Lake---NOT WORKING
query = parsed_df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/tmp/delta_checkpoint/") \
    .option("path", "/tmp/delta_table/") \
    .outputMode("append") \
    .start()'''

'''
# To get data in Terminal
query = parsed_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()
'''

# Allow the stream to run for a short duration
time.sleep(15)  # Adjust this duration based on your requirements
# Stop the streaming query
query.stop()

query.awaitTermination()
