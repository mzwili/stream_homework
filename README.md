🟢 stream_homework — Data Engineering Zoomcamp Module 7 (Streaming with PyFlink)
Project Overview

This project contains the homework solution for Module 7: Streaming with Kafka (Redpanda) and PyFlink in the Data Engineering Zoomcamp
.

We simulate real-time taxi data processing using Green Taxi October 2025 dataset. The project covers:

Streaming data ingestion with Kafka (Redpanda)
Building Python producers and consumers
PyFlink streaming jobs using tumbling and session windows
Writing results to PostgreSQL
Monitoring via Flink UI
📁 Project Structure
07-streaming/
└── workshop/
    ├── docker-compose.yaml           # Docker Compose setup (Redpanda, Flink, Postgres)
    ├── Dockerfile.flink              # Flink container build
    ├── Dockerfile.kafka              # Redpanda container build
    ├── src/
    │   ├── producer/
    │   │   └── green_producer.py    # Reads Parquet and sends to Kafka topic
    │   ├── consumer/
    │   │   └── green_consumer.py    # Consumes messages from Kafka
    │   └── job/
    │       ├── tumbling_job.py       # 5-min tumbling window per pickup location
    │       ├── session_job.py        # Session window analysis per pickup location
    │       └── tips_job.py           # 1-hour tumbling window for total tips
    ├── data/
    │   └── green_tripdata_2025-10.parquet  # Green Taxi dataset
    └── README.md                     # This file
⚙️ Setup Instructions
1. Clone Repository
git clone https://github.com/mzwili/stream_homework.git
cd stream_homework/workshop
2. Download Dataset
mkdir -p data
wget -P data https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet
3. Create Python Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
4. Start Docker Infrastructure
docker compose down -v
docker compose build
docker compose up -d

Services included:

Redpanda (Kafka) — localhost:9092
Flink Job Manager — http://localhost:8081
Flink Task Manager
PostgreSQL — localhost:5432 (user: postgres, password: postgres)
5. Verify Services
docker ps

Check:

stream_homework-redpanda-1
stream_homework-jobmanager-1
stream_homework-taskmanager-1
stream_homework-postgres-1
📝 How to Run
1️⃣ Producer
python src/producer/green_producer.py

Sends green taxi data to Kafka topic green-trips.

2️⃣ Consumer (Optional)
python src/consumer/green_consumer.py

Reads all messages from green-trips and performs analysis (e.g., trips with distance > 5 km).

3️⃣ Flink Jobs

Submit each job to Flink Job Manager:

docker exec -it stream_homework-jobmanager-1 flink run -py /opt/src/job/q4_tumbling.py
docker exec -it stream_homework-jobmanager-1 flink run -py /opt/src/job/q5_session.py
docker exec -it stream_homework-jobmanager-1 flink run -py /opt/src/job/q6_tips.py
Table results are written to PostgreSQL
Check results via:
SELECT * FROM <your_table_name> LIMIT 10;
✅ Key Concepts Covered
Kafka producer/consumer
PyFlink tumbling windows and session windows
Streaming with event-time and watermarks
Writing results to PostgreSQL
Dockerized environment for Flink + Kafka + PostgreSQL
📌 References
Data Engineering Zoomcamp Module 7
Apache Flink Documentation
Kafka / Redpanda Documentation
🚀 Optional Next Steps
Add Dockerfile for Python dependencies
Automate producer + Flink job execution with Makefile
Add unit tests for producer/consumer