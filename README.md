# Real-Time-Stock-Market-Data-Pipeline
  kafka_spark_airflow_venv

* Project Overview
  This project implements an end-to-end real-time data pipeline that ingests stock market data from an external API, streams it via Apache Kafka, processes it using Apache Spark in Databricks, and orchestrates tasks using Apache Airflow. The processed data is stored in Delta Lake and visualized using Databricks SQL.

* Tech Stack Overview
  Python: Used to fetch stock market data from the API.
  Kafka: Facilitates real-time data ingestion and streaming.
  Spark (Structured Streaming): Handles real-time data processing.
  Databricks: Provides data storage (Delta Lake) and visualization capabilities.
  Airflow: Manages orchestration and scheduling of tasks.
  PostgreSQL: Stores historical aggregated data.
  Virtual Environment: Creates an isolated development setup.


* Architecture Diagram

                        ┌────────────────────────────────────┐
                        │ External Stock API (https://       │
                        │  finnhub.io/)                      │
                        └───────────────┬────────────────────┘
                                        │ (JSON Data via API)
                                        ▼
                        ┌────────────────────────────────┐
                        │   Kafka Producer (Python)      │
                        │ - Fetches API data every sec   │
                        │ - Publishes to 'stock_topic'   │
                        └───────────────┬────────────────┘
                                        │
                                        ▼
                        ┌────────────────────────────────┐
                        │   Kafka Broker & Topic         │
                        │ - Stores live stock data       │
                        │ - Allows Spark to consume      │
                        └───────────────┬────────────────┘
                                        │
                                        ▼
                      ┌───────────────────────────────────────┐
                      │      Spark Structured Streaming       │
                      │  - Reads from 'stock_topic'           │
                      │ - Cleans, enriches data               │
                      │ - Writes to Delta Lake                │
                      └───────────────┬────────────────────── ┘
                                      │
                                      ▼
          
                      ┌────────────────────────────────────┐
                      │        Airflow DAG (Orchestration) │
                      │ - Starts Kafka producer            │
                      │ - Triggers Spark processing job    │
                      │ - Moves data to PostgreSQL         │
                      └────────────────────────────────────┘


* Steps to Implement the Project

  Step 1: Set Up a Virtual Environment
  
      # Create a virtual environment
      python3 -m venv kafka_airflow_spark_env

      # Activate environment
      source kafka_airflow_spark_env/bin/activate  # For Mac/Linux
      # On Windows: kafka_airflow_spark_env\Scripts\activate

      # Install required packages
      pip install kafka-python apache-airflow apache-spark requests pandas psycopg2-binary

      # Alternate for apache-spark
      pip install pyspark
      # To check installation: python -c "import pyspark; print(pyspark.__version__)"
      # or
      # spark-submit --version


  Step 2: Install Zookeeper and Kafka (Outside the Virtual Environment)
      deactivate # to deactivate venv
      brew install zookeeper
      brew install kafka

      # Start Zookeeper and Kafka

      # Start Zookeeper:
      zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties &  # When you append & to a command, it runs the command in the background
      Or
      brew services restart zookeeper # without showing background running process

      # Start Kafka:
      kafka-server-start /usr/local/etc/kafka/server.properties &
      or 
      brew services restart kafka # without showing background running process

  Step 3: Manage Kafka
      To stop Kafka and Zookeeper:
      brew services stop kafka
      brew services stop zookeeper

      To delete Kafka log directory:
      rm -rf /usr/local/var/lib/kafka-logs

      To use the Zookeeper CLI tool:
      zkCli -server localhost:2181

      To manage Kafka topics:
      # To delete topic
      kafka-topics --delete --topic stock_topic --bootstrap-server localhost:9092 
      # To list Kafka topics
      kafka-topics --list --bootstrap-server localhost:9092 
      # make sure listeners=PLAINTEXT://localhost:9092 is uncomment

      # to check apache spark port 
      lsof -i -P | grep LISTEN | grep 404

  Step 4: Set Up PostgreSQL

      # Download PostgreSQL JDBC driver
      wget -P ~/kafka_airflow_spark_env/kafka_airflow_spark_env https://jdbc.postgresql.org/download/postgresql-42.5.1.jar

      # Install Delta Lake for Spark
      pip install pyspark delta-spark

      # To confirm that Delta Lake is installed, open PySpark shell and run:
      pyspark --packages io.delta:delta-core_2.12:2.4.0
      # Then inside PySpark, run:
      spark.read.format("delta")

      # To open and create a database and table in PostgreSQL (in Terminal)

      psql -h localhost -p 5432 -U postgres

      CREATE DATABASE stocks_db;
      \l
      \c stocks_db;
      CREATE TABLE stocks_data (
          symbol TEXT,
          price FLOAT,
          high FLOAT,
          low FLOAT,
          open FLOAT,
          timestamp TIMESTAMP
      );

  Step 5: Initialize and Run Apache Airflow

      pip install apache-airflow
      airflow db init
      airflow webserver --port 8080 & # If port is busy, use another (e.g., 8081)

      # Create a user with a password
      airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --email admin@example.com \
        --role Admin \
        --password yourpassword

      airflow scheduler 

      #Additional Information
      TO upgrade Airflow:
      pip install --upgrade apache-airflow

      #restart everything
      pkill -f airflow
      airflow db reset  # This wilyl erase all DAG runs!
      airflow db init

      #To uninstall Airflow:
      pip uninstall apache-airflow -y
      rm -rf ~/airflow
      deactivate # venv
      source kafka_airflow_spark_env/bin/activate
      pip cache purge # Clean Up Python Cache
      # Verify Airflow is Removed
      airflow version


Prerequisites: Before running this project, ensure the following services are up and running in the given order:
1. Start Zookeeper
2. Start Kafka Broker
3. Start Airflow Scheduler (For orchestrating tasks)
4. Start Airflow Webserver

   
============================================
* Apache Spark in Databricks is the most efficient way to process the data because Spark allows for distributed computing. 
Pandas, on the other hand, is limited to in-memory processing and will not perform efficiently for very large datasets.

* Setting Up Databricks (Free Community Edition)

Follow these steps to set up Databricks for processing stock market data:

1. Sign Up for Databricks Community Edition
    Go to Databricks Community Edition and sign up.
    This allows free usage with limited resources.

2. Create and Configure a Cluster
    Navigate to Compute.
    Click Create Cluster.
    Give your cluster a meaningful name.
    Click the Create button to launch the cluster.

3. Create a Notebook
    Go to Workspace → Your Workspace.
    Click Create → Folder and name it (e.g., "Stock_Analysis").
    Inside the folder, click Create → Notebook.
    Name your notebook (e.g., "Kafka_Spark_Streaming").
    Select a cluster to attach the notebook.

4. Install Kafka Libraries in Databricks
    Open the Compute tab and select the created cluster.
    Go to Libraries → Install New.
    Choose Maven as the library source.
    Search for spark-sql-kafka in Maven packages.
    Select:

    org.apache.spark    spark-sql-kafka-0-10_2.12    3.5.4

    (Ensure this matches your Spark version)
    Click Install and wait for the installation to complete.
    Restart the cluster.

5. Verify Kafka Library Installation
    Run the following command in a Databricks notebook to confirm that the Kafka package is properly loaded:

    print(spark.conf.get("spark.jars.packages"))
    Also, import necessary PySpark functions:

    from pyspark.sql import functions as F

6. Enable Databricks File System (DBFS)
    Go to Databricks Workspace.
    Click on your User Profile or Settings.
    Look for the DBFS File Browser option (toggle switch).
    Enable it.

7. Access the Databricks Catalog
    Navigate to the Catalog section to manage databases and tables in Delta Lake.
