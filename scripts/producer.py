import json
import time
import requests
from kafka import KafkaProducer

# Kafka Config
KAFKA_TOPIC = 'stock-topic-1'
KAFKA_SERVER = 'localhost:9092'
FINNHUB_API_KEY = ""  # Replace with your Finnhub API key

# Set up Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON data
)

def fetch_stock_price(symbol="AAPL"):
    """Fetch stock market data from Finnhub API"""
    
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Extract the relevant stock data
            stock_data = {
                "symbol": symbol,
                "price": data["c"],  # 'c' is the current price
                "high": data["h"],   # 'h' is the high price of the day
                "low": data["l"],    # 'l' is the low price of the day
                "open": data["o"],   # 'o' is the opening price
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            return stock_data

        return {"symbol": symbol, "error": "Invalid API response"}

    except requests.exceptions.RequestException as e:
        return {"symbol": symbol, "error": str(e)}

# For Continue Fetching Data
# while True:
#     stock_data = fetch_stock_price("AAPL")  # Fetch Apple stock data
#     print(f"Fetched Data: {stock_data}")  # Debugging
#     producer.send(KAFKA_TOPIC, stock_data)  # Send data to Kafka topic
#     print(f"Sent: {stock_data}")  # Print the sent message
#     time.sleep(20)  # Fetch data every 5 seconds


count = 0
max_records = 10  # Stop after sending 10 messages

while count < max_records:
    stock_data = fetch_stock_price("AAPL")  # Fetch Apple stock data
    print(f"Fetched Data: {stock_data}")  # Debugging
    producer.send(KAFKA_TOPIC, stock_data)  # Send data to Kafka topic
    print(f"Sent: {stock_data}")  # Print the sent message
    count += 1
    time.sleep(5)  # Fetch data every 5 seconds

print("Finished sending 10 records.")
producer.close()