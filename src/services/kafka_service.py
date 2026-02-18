from kafka import KafkaProducer,KafkaConsumer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def publish_event(topic, payload):
    try:    
        producer.send(topic, payload)
        producer.flush()
    except Exception as e:
        raise Exception(f"Error publishing to Kafka: {e}")

