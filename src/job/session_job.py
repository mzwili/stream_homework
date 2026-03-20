t_env.execute_sql("""
CREATE TABLE session_results (
    PULocationID INT,
    num_trips BIGINT
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'session_results',
    'username' = 'postgres',
    'password' = 'postgres'
)
""")

t_env.execute_sql("""
INSERT INTO session_results
SELECT
    PULocationID,
    COUNT(*) as num_trips
FROM TABLE(
    SESSION(TABLE green_trips, DESCRIPTOR(event_time), INTERVAL '5' MINUTES)
)
GROUP BY PULocationID, window_start, window_end
""")