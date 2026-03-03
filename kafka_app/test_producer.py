from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

for i in range(13,22):
    message = {"id": i, "text": f"Hello Kafka #{i}"}
    producer.send("test-topic", value=message)
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()
producer.close()
print("Producer finished.")
