import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "green-trips",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

count = 0

for message in consumer:
    trip = message.value

    if trip["trip_distance"] and float(trip["trip_distance"]) > 5:
        count += 1

print("Trips > 5km:", count)