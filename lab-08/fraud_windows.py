from pyflink.table import EnvironmentSettings, TableEnvironment

env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

# Один читатель на 3 партиции: иначе лишние idle-читатели
# держат watermark на -бесконечности и окна никогда не закрываются
t_env.get_config().get_configuration().set_string("parallelism.default", "1")

# Подключаем Kafka-коннектор
t_env.get_config().get_configuration().set_string(
    "pipeline.jars",
    "file:///home/giga/datashop-platform/lab-08/flink-sql-connector-kafka-3.2.0-1.19.jar"
)

t_env.execute_sql("""
    CREATE TABLE payment_transactions (
        transaction_id STRING,
        customer_id STRING,
        category STRING,
        amount DOUBLE,
        country STRING,
        status STRING,
        `timestamp` BIGINT,
        event_time AS TO_TIMESTAMP_LTZ(`timestamp`, 3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'payment_transactions',
        'properties.bootstrap.servers' = 'localhost:9092',
        'properties.group.id' = 'flink-fraud-detector',
        'scan.startup.mode' = 'latest-offset',
        'format' = 'json'
    )
""")

t_env.execute_sql("""
    CREATE TABLE fraud_alerts (
        window_start TIMESTAMP(3),
        window_end TIMESTAMP(3),
        customer_id STRING,
        total_spent DOUBLE,
        transaction_count BIGINT
    ) WITH ('connector' = 'print')
""")

t_env.execute_sql("""
    INSERT INTO fraud_alerts
    SELECT
        TUMBLE_START(event_time, INTERVAL '5' MINUTE) AS window_start,
        TUMBLE_END(event_time, INTERVAL '5' MINUTE) AS window_end,
        customer_id,
        SUM(amount) AS total_spent,
        COUNT(*) AS transaction_count
    FROM payment_transactions
    WHERE status = 'completed'
    GROUP BY
        TUMBLE(event_time, INTERVAL '5' MINUTE),
        customer_id
    HAVING SUM(amount) > 500
""").wait()
