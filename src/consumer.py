from kafka import KafkaConsumer
import json
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()

from services.kafka_service import consume_events

if __name__ == '__main__':
    print("Consumer started. Listening to weather-events")
    consume_events('weather-events')