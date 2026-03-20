t_env.execute_sql("""
CREATE TABLE tips_hourly (
    window_start TIMESTAMP(3),
    total_tips DOUBLE
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'tips_hourly',
    'username' = 'postgres',
    'password' = 'postgres'
)
""")

t_env.execute_sql("""
INSERT INTO tips_hourly
SELECT
    window_start,
    SUM(tip_amount) as total_tips
FROM TABLE(
    TUMBLE(TABLE green_trips, DESCRIPTOR(event_time), INTERVAL '1' HOUR)
)
GROUP BY window_start
""")