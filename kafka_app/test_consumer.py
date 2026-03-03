from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "test-topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="test-group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("Listening on 'test-topic'... (Ctrl+C to stop)")
for message in consumer:
    print(f"Received: {message.value}")
