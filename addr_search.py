import os

import requests

API_KEY = os.getenv("GEOCODE_API_KEY")

result = requests.get(f"https://geocode.maps.co/search?q=123 main st, springfield, or &api_key={API_KEY}")
print(f"result was: {str(result.text)}")