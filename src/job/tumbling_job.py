from pyflink.table import EnvironmentSettings, TableEnvironment

env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

t_env.get_config().set("parallelism.default", "1")

# SOURCE
t_env.execute_sql("""
CREATE TABLE green_trips (
    lpep_pickup_datetime STRING,
    PULocationID INT,
    event_time AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'green-trips',
    'properties.bootstrap.servers' = 'redpanda:9092',
    'format' = 'json',
    'scan.startup.mode' = 'earliest-offset'
)
""")

# SINK (Postgres)
t_env.execute_sql("""
CREATE TABLE trips_window (
    window_start TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'trips_window',
    'username' = 'postgres',
    'password' = 'postgres'
)
""")

# QUERY
t_env.execute_sql("""
INSERT INTO trips_window
SELECT
    window_start,
    PULocationID,
    COUNT(*) as num_trips
FROM TABLE(
    TUMBLE(TABLE green_trips, DESCRIPTOR(event_time), INTERVAL '5' MINUTES)
)
GROUP BY window_start, PULocationID
""")