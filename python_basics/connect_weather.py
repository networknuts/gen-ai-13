import requests
from dotenv import load_dotenv
import os

# READ THE .ENV FILE
load_dotenv()

# DECLARED URL VARIABLES
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
OPENWEATHERMAP_ZIP_CODE = input("Enter your zip code: ")
OPENWEATHERMAP_COUNTRY_CODE = input("Enter your country code: ")

# CREATED THE URL
OPENWEATHERMAP_URL = f"https://api.openweathermap.org/data/2.5/weather?zip={OPENWEATHERMAP_ZIP_CODE},{OPENWEATHERMAP_COUNTRY_CODE}&appid={OPENWEATHERMAP_API_KEY}"

# CONNECTING TO THE URL
response = requests.get(OPENWEATHERMAP_URL)

# PRINT URL STATUS CODE
print(response.status_code)

# PRINT THE URL RESPONSE
print(response.json())