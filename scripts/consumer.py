### FILE NOT IN USE ###

import json
from kafka import KafkaConsumer

# Kafka consumer configuration
consumer = KafkaConsumer(
    'stock-topic-1',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # Deserialize JSON messages
)

def consume_messages():
    """Consume messages from Kafka topic"""
    for message in consumer:
        stock_data = message.value
        print(f"Consumed: {stock_data}")

        # Handle errors properly
        if "error" in stock_data:
            print("⚠️ ERROR in fetched data:", stock_data["error"])
        else:
            print(f"✅ Received Stock Data: {stock_data}")

consume_messages()
