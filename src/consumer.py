from kafka import KafkaConsumer
import json
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('SUPABASE_KEY')
url = os.getenv('URL_SUPABASE')

supabase = create_client(url, api_key)

consumer = KafkaConsumer(
    'weather-events',
    group_id='weather-consumer-group',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def consume_events(topic):
    for message in consumer:
        try:
            event = message.value
            supabase.table('weather_readings').insert(event).execute()
        except Exception as e:
            print(f"Error processing message: {e}")

if __name__ == '__main__':
    print("Consumer started. Listening to weather-events")
    consume_events('weather-events')