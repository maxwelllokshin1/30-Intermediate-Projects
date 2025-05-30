import requests
from geopy.geocoders import Nominatim
import datetime

base_url = "http://api.open-meteo.com/v1/forecast"

def get_info(params):
    url = f"{base_url}"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data {response.status_code}")

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="locationLL")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def main():
    cur_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:00")
    state = input("State Name: ")
    city = input("City Name: ")
    location = state + " " + city
    latitude, longitude = get_coordinates(location)

    if not latitude or not longitude:
        print(f"Could not find coordinates for {city}")
        return

    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "hourly": "temperature_2m",
        "temperature_unit": "fahrenheit",
        "start_hour": cur_datetime,
        "end_hour": cur_datetime,
        "timezone": "EST",
    }
    data = get_info(params)
    if not data:
        return
    current_day = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M")
    print(f"The temperature for {city}, {state} on {current_day} at {current_time} is:" \
          f"\n{data['hourly']['temperature_2m']} {data['hourly_units']['temperature_2m']}")

if __name__ == "__main__":
    main()
