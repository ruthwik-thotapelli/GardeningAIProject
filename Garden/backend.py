from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

last_weather = {}

def get_weather_description(code):
    desc_map = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle",
        53: "Moderate drizzle", 55: "Dense drizzle", 61: "Slight rain",
        63: "Moderate rain", 65: "Heavy rain", 71: "Slight snow",
        73: "Moderate snow", 75: "Heavy snow", 95: "Thunderstorm"
    }
    return desc_map.get(code, "Unknown")

def extract_space_and_location(user_input):
    user_input = user_input.lower()
    space_keywords = ["balcony", "small", "room", "corner", "backyard", "large", "garden", "tiny"]

    match = re.search(r'(\d{1,2})\s*x\s*(\d{1,2})', user_input)
    space = ""
    if match:
        space = f"{match.group(1)}x{match.group(2)}"
    else:
        for word in space_keywords:
            if word in user_input:
                space = word
                break

    loc_match = re.search(r'(?:climate|weather)?\s*in\s*([a-zA-Z ]+)', user_input)
    if loc_match:
        location = loc_match.group(1).strip()
    elif "climate" in user_input or "weather" in user_input:
        location = user_input.replace("climate", "").replace("weather", "").replace("in", "").strip()
    else:
        location = user_input.strip()

    return location, space

def suggest_plants_by_conditions(temperature, humidity, description, space):
    space_keywords = space.lower()
    plant_sets = {
        "dry_hot": ["Aloe Vera", "Bougainvillea", "Cactus", "Marigold", "Jasmine"],
        "humid": ["Ferns", "Money Plant", "Areca Palm", "Calathea", "Bamboo Palm"],
        "cool": ["Lavender", "Mint", "Chrysanthemum", "Daffodil", "Foxglove"],
        "small_space": ["Snake Plant", "Spider Plant", "Peace Lily", "Pothos", "ZZ Plant"],
        "large_space": ["Tomato", "Hibiscus", "Tulsi", "Brinjal", "Papaya"]
    }

    suggestions = []

    if temperature > 30 and humidity < 50:
        suggestions += plant_sets["dry_hot"]
    elif humidity > 70:
        suggestions += plant_sets["humid"]
    elif temperature < 20:
        suggestions += plant_sets["cool"]

    if any(word in space_keywords for word in ["balcony", "small", "room", "3x3", "corner", "4x2", "2x2"]):
        suggestions += plant_sets["small_space"]
    elif any(word in space_keywords for word in ["backyard", "large", "garden", "4x4", "big space", "14x12", "9x3"]):
        suggestions += plant_sets["large_space"]

    return list(set(suggestions)) if suggestions else ["Succulents", "Money Plant", "Ferns"]

@app.route('/chat', methods=['POST'])
def chatbot():
    global last_weather
    try:
        data = request.get_json()
        user_input = data.get('message', '').lower()

        greetings = ["hi", "hello", "hey", "whatsup", "what's up"]
        if any(user_input.strip() == greet for greet in greetings):
            return jsonify({"reply": "I'm here to help you with gardening! Ask about the climate or your space (e.g. 3x3 area, balcony, backyard)."})

        location, space = extract_space_and_location(user_input)

        if location and not space:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
            geo_response = requests.get(geo_url).json()

            if 'results' not in geo_response or len(geo_response['results']) == 0:
                return jsonify({"reply": f"❌ Could not find the location: {location}"})

            lat = geo_response['results'][0]['latitude']
            lon = geo_response['results'][0]['longitude']

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weathercode"
            weather_response = requests.get(weather_url).json()

            try:
                current = weather_response['current']
                temperature = current['temperature_2m']
                humidity = current['relative_humidity_2m']
                code = current['weathercode']
            except KeyError:
                return jsonify({"reply": "❌ Error fetching weather data."})

            description = get_weather_description(code)
            last_weather = {"temperature": temperature, "humidity": humidity, "description": description}

            return jsonify({
                "reply": f"Temp: {temperature}°C  Humidity: {humidity}%  Condition: {description}\n\nNow tell me about your space!"
            })

        elif space and last_weather:
            suggestions = suggest_plants_by_conditions(
                last_weather['temperature'],
                last_weather['humidity'],
                last_weather['description'],
                space
            )
            return jsonify({"reply": "Suitable plants: " + ", ".join(suggestions)})

        else:
            return jsonify({"reply": "Please ask about the climate or describe your space like 'balcony', '3x3 area', or 'backyard'."})

    except Exception as e:
        print("❌ Backend Error:", e)
        return jsonify({"reply": "❌ Server error. Please try again later."})

if __name__ == '__main__':
    app.run(debug=True)
