from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(env)

t_env.execute_sql("""
     CREATE TABLE weather_events (
        event_id STRING,
        city_id INT,
        city_name STRING,
        description STRING,
        event_timestamp STRING
    )  WITH (
        'connector' = 'kafka',
        'topic' = 'weather-events',
        'properties.bootstrap.servers' = 'kafka:29092',
        'properties.group.id' = 'flink-consumer',
        'scan.startup.mode' = 'latest-offset',
        'format' = 'json'
    )
""")

t_env.execute_sql("""
    CREATE TABLE rain_alerts (
        event_id STRING,
        city_id INT,
        city_name STRING,
        description STRING,
        event_timestamp STRING)
    WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://openweather-airflow-db-1:5432/airflow',
        'table-name' = 'rain_alerts',
        'username' = 'airflow',
        'password' = 'airflow')
""") 

result = t_env.execute_sql("""insert into rain_alerts select * from weather_events where description like '%rain%'""")
result.wait() #impede que o job morra imediatamente, aguardando a conclusão da inserção dos dados filtrados na tabela rain_alerts.