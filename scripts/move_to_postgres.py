from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import TimestampType


# Initialize Spark Session
spark = SparkSession.builder \
    .appName("ParquetToPostgres") \
    .config("spark.jars", "/Users/kafka_airflow_spark_venv/postgresql-42.5.1.jar") \
    .getOrCreate()

# Load Parquet file into DataFrame
df = spark.read.parquet("/Users/kafka_airflow_spark_venv/Parquet_Data/parquet_table")

# Convert 'timestamp' column to TimestampType
df = df.withColumn("timestamp", col("timestamp").cast(TimestampType()))

# Show schema
df.printSchema()

# PostgreSQL Configuration
POSTGRES_URL = "jdbc:postgresql://localhost:5432/stocks_db"
POSTGRES_USER = "username"
POSTGRES_PASSWORD = "password"
POSTGRES_TABLE = "stocks_data"


df.write \
    .format("jdbc") \
    .option("url", POSTGRES_URL) \
    .option("dbtable", POSTGRES_TABLE) \
    .option("user", POSTGRES_USER) \
    .option("password", POSTGRES_PASSWORD) \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

print("Data moved to PostgreSQL successfully!")

spark.stop()
