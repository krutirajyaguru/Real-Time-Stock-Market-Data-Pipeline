import subprocess
import time

# Kafka configuration
ZOOKEEPER_CONFIG = "/usr/local/etc/kafka/zookeeper.properties"
#Run this command to check if Kafka is installed via Homebrew: brew info kafka
#brew services start kafka
KAFKA_CONFIG = "/usr/local/etc/kafka/server.properties"
KAFKA_TOPIC = "stock-topic-1"
BOOTSTRAP_SERVER = "localhost:9092"

def start_zookeeper():
    """Start Zookeeper Server"""
    print("Starting Zookeeper...")
    subprocess.Popen(["zookeeper-server-start", ZOOKEEPER_CONFIG], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Wait for Zookeeper to start

def start_kafka():
    """Start Kafka Broker"""
    print("Starting Kafka Broker...")
    subprocess.Popen(["kafka-server-start", KAFKA_CONFIG], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Wait for Kafka to start

def create_kafka_topic():
    """Create Kafka topic if it doesn't exist"""
    print(f"Creating Kafka topic: {KAFKA_TOPIC}...")
    cmd = [
        "kafka-topics", "--create", "--if-not-exists",
        "--topic", KAFKA_TOPIC,
        "--bootstrap-server", BOOTSTRAP_SERVER,
        "--partitions", "3",
        "--replication-factor", "1"
    ]
    subprocess.run(cmd)

# Start everything
start_zookeeper()
start_kafka()
create_kafka_topic()

print("Kafka setup complete!")
