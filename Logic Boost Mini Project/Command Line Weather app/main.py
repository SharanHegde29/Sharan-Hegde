import requests
import sys

BASE_URL = 'https://api.open-meteo.com/v1/forecast'
GEOCODING_URL = 'https://geocoding-api.open-meteo.com/v1/search'


def get_coordinates_from_city(city_name):
    params = {
        'name': city_name,
        'count': 1,
        'language': 'en',
        'format': 'json'
    }
    
    try:
        response = requests.get(GEOCODING_URL, params=params)
        response.raise_for_status()

        data = response.json()
        
        if data.get('results'):
            first_result = data['results'][0]
            latitude = first_result.get('latitude')
            longitude = first_result.get('longitude')
            full_name = first_result.get('name') 
            
            country = first_result.get('country')
            admin1 = first_result.get('admin1')
            
            display_name = full_name
            if admin1 and country:
                display_name = f"{full_name}, {admin1}, {country}"
            elif country:
                display_name = f"{full_name}, {country}"

            return latitude, longitude, display_name
        else:
            print(f"No results found for '{city_name}'.")
            return None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the geocoding service: {e}")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred during geocoding: {e}")
        return None, None, None


def get_weather(latitude, longitude):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m,relative_humidity_2m,weather_code', 
        'temperature_unit': 'celsius', 
        'timeformat': 'unixtime',
        'timezone': 'auto'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()

        def get_description_from_code(code):
            wmo_codes = {
                0: "Clear sky",
                1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing rime fog",
                51: "Drizzle: Light", 53: "Drizzle: Moderate", 55: "Drizzle: Dense",
                61: "Rain: Slight", 63: "Rain: Moderate", 65: "Rain: Heavy",
                71: "Snow fall: Slight", 73: "Snow fall: Moderate", 75: "Snow fall: Heavy",
                80: "Rain showers: Slight", 81: "Rain showers: Moderate", 82: "Rain showers: Violent",
                95: "Thunderstorm: Slight or moderate",
                96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
            }
            return wmo_codes.get(code, "Unknown condition")

        current = data.get('current', {})
        
        weather_info = {
            'location_str': f"Lat: {latitude:.4f}, Lon: {longitude:.4f}",
            'temperature': current.get('temperature_2m'),
            'humidity': current.get('relative_humidity_2m'),
            'description': get_description_from_code(current.get('weather_code'))
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the weather service: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def display_weather(weather_data, location_name=""):
    if not weather_data:
        return

    display_location = location_name if location_name else weather_data.get('location_str', 'Unknown Location')
    
    temp = weather_data.get('temperature')
    desc = weather_data.get('description')
    humidity = weather_data.get('humidity')
    
    temp_str = f"{temp}°C" if temp is not None else "N/A"
    humidity_str = f"{humidity}%" if humidity is not None else "N/A"
    
    print("-" * 30)
    print(f"Weather at {display_location}")
    print("-" * 30)
    print(f"Temperature: {temp_str}")
    print(f"Description: {desc}")
    print(f"Humidity:    {humidity_str}")
    print("-" * 30)

def main():
    try:
        city_name = input("Enter the city name: ")
    except EOFError:
        print("\nInput cancelled. Exiting.")
        sys.exit(1)
        
    if not city_name.strip():
        print("No city name entered. Exiting.")
        sys.exit(1)

    latitude, longitude, display_location = get_coordinates_from_city(city_name)
    
    if latitude is None or longitude is None:
        print("Could not retrieve coordinates. Aborting weather fetch.")
        return

    print(f"Fetching weather for: {display_location}...")
    
    weather_data = get_weather(latitude, longitude)
    
    display_weather(weather_data, display_location)

if __name__ == "__main__":
    main()