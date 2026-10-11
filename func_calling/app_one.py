import os 
import requests
from dotenv import load_dotenv
from openai import OpenAI
import json


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

# MAKE THE FIRST LLM CALL
response = client.responses.create(
    model="gpt-6-luna",
    input=human_query,
    tools=openai_tools
)

# LOGIC FOR FUNCTION EXECUTED
function_output = []

for item in response.output:
    if item.type == "function_call":
        arguments = json.loads(item.arguments) # str to dict
        if item.name == "get_weather":
            result = get_weather(arguments['zipcode'])
            print("RAW FUNCTION OUTPUT")
            print(result)
            print("="*25)
        else:
            result = "unknown function called"

        function_output.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps({"result": result}) #dict to str
        })

# SECOND LLM CALL
final_response = client.responses.create(
    model="gpt-6-luna",
    input=function_output,
    previous_response_id=response.id
)

print("\nAI SUMMARIZED OUTPUT\n")
print(final_response.output_text)