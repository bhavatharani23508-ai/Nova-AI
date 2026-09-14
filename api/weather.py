import requests


def get_weather(city):

    # Step 1: Find the city's latitude and longitude
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(
        geocoding_url,
        params=geocoding_params,
        timeout=10
    )

    data = response.json()

    if "results" not in data:
        return f"Sorry, I couldn't find the city '{city}'."

    location = data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    city_name = location["name"]
    country = location.get("country", "")

    # Step 2: Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    weather_data = weather_response.json()
    current = weather_data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind_speed = current["wind_speed_10m"]

    return f"""
### 🌦️ Weather in {city_name}, {country}

**Temperature:** {temperature} °C

**Humidity:** {humidity}%

**Wind Speed:** {wind_speed} km/h
"""
