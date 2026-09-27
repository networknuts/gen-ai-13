import requests
import os
import json

def talk_to_ai(human_query,human_name):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_URL = "https://api.openai.com/v1/responses"
    OPENAI_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    OPENAI_DATA = {"model":"gpt-6-luna","input":human_query}
    result = requests.post(OPENAI_URL,headers=OPENAI_HEADERS,data=json.dumps(OPENAI_DATA))
    response = result.json()['output'][1]['content'][0]['text']
    return {
        "LLM Response": response,
        "Model": "gpt-6-luna",
        "User": human_name
    }