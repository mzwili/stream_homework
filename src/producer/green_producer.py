import json
import pandas as pd
from kafka import KafkaProducer
from time import time

df = pd.read_parquet("../data/green_tripdata_2025-10.parquet")

df = df[[
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "passenger_count",
    "trip_distance",
    "tip_amount",
    "total_amount"
]]

df["lpep_pickup_datetime"] = df["lpep_pickup_datetime"].astype(str)
df["lpep_dropoff_datetime"] = df["lpep_dropoff_datetime"].astype(str)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

t0 = time()

for record in df.to_dict(orient="records"):
    producer.send("green-trips", value=record)

producer.flush()

t1 = time()

print(f"Took {(t1 - t0):.2f} seconds")