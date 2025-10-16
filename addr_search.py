import os
import json
import requests

API_KEY = os.getenv("GEOCODE_API_KEY")

#result = requests.get(f"https://geocode.maps.co/search?q=123 main st, springfield, or &api_key={API_KEY}")
#print(f"result was: {str(result.text)}")

def get_lat_lon(address_string):
    url = "https://geocode.maps.co/search?q=" + address_string + "&api_key=" + API_KEY
    result = requests.get(url)
    result_data = result.text
    result_parsed = json.loads(result_data)
    print(f"lat was: {result_parsed[0]["lat"]}")
    print(f"lon was: {result_parsed[0]["lon"]}")
    lat_lon = [float(result_parsed[0]["lat"]), float(result_parsed[0]["lon"])]
    return lat_lon


