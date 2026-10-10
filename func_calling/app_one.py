import os 
import requests
from dotenv import load_dotenv
from openai import OpenAI


# SETUP THE ENVIRONMENT
load_dotenv()
f = open("weather_func_description.txt","r")
weather_func_description = f.read()
f.close()
client = OpenAI()

# CREATE THE TOOL / FUNCTION
def get_weather(zipcode):
    country_code = "in"
    openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{country_code}&appid={openweathermap_api_key}"
    response = requests.get(url)
    result = response.json()
    return result 

# FUNCTION SCHEMA / BLUEPRINT
openai_tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": weather_func_description,
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "The zipcode of the location to get the weather of."
                },
            },
            "required": ["zipcode"],
        },
    },
]

# ASK FOR CUSTOMER QUERY
human_query = input("Enter your query: ")

# MAKE THE LLM CALL
response = client.responses.create(
    model="gpt-6-luna",
    input=human_query,
    tools=openai_tools
)

print(response.output)