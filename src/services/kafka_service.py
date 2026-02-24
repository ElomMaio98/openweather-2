from kafka import KafkaProducer,KafkaConsumer
import json
from supabase import create_client
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


api_key = os.getenv('SUPABASE_KEY')
url = os.getenv('URL_SUPABASE')

supabase = create_client(url, api_key)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

consumer = KafkaConsumer(
    'weather-events',
    group_id='weather-consumer-group',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


def publish_event(topic, payload):
    try:    
        producer.send(topic, payload)
        producer.flush()
    except Exception as e:
        raise Exception(f"Error publishing to Kafka: {e}")

def consume_events(topic):
    for message in consumer:
        try:
            event = message.value
            supabase.table('weather_readings').insert(event).execute()
        except Exception as e:
            print(f"Error processing message: {e}")