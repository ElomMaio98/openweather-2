from flask import Flask, jsonify, request
from supabase import create_client
import os
import uuid
from datetime import datetime
from services.weather_service import get_weather
from services.kafka_service import publish_event
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('SUPABASE_KEY')
url = os.getenv('URL_SUPABASE')

supabase = create_client(url, api_key)
def create_app() -> Flask:
    app = Flask(__name__)
    @app.route('/weather', methods=['POST'])
    def fetch_weather():
        city_id = request.args.get('city_id')
        if not city_id:
            return jsonify({"error": "city_id is required"}), 400
        try: 
            result = supabase.table('cities').select('*').eq('id', city_id).eq('active', True).execute()
            if not result.data:
                return jsonify({"error": "City not found or inactive"}), 404
            city = result.data[0]
            weather = get_weather(city['latitude'], city['longitude'])
            event = {
                "event_id": str(uuid.uuid4()),
                "event_timestamp": datetime.now().isoformat(),
                "city_id": city['id'],
                "city_name": city['name'],
                **weather
            }
            publish_event('weather-events', event)
            return jsonify({"status": "accepted", "event_id": event["event_id"]}), 202
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)