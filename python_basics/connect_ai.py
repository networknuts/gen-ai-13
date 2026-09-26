import requests
from dotenv import load_dotenv
import os
import json

# STEP 1: LOAD THE .ENV FILE
load_dotenv()

# STEP 2: ASK FOR CUSTOMER QUERY
human_query = input("Enter your query: ")

# STEP 3: DECLARE THE OPENAI API KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# STEP 4: SET THE OPENAI URL
OPENAI_URL = "https://api.openai.com/v1/responses"

# STEP 5: ASSIGN HEADERS
OPENAI_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# STEP 7: DEFINE THE PAYLOAD / DATA
OPENAI_DATA = {"model":"gpt-6-luna","input":human_query}

# STEP 8: MAKE CONNECTION AND PRINT RESPONSE
response = requests.post(OPENAI_URL,headers=OPENAI_HEADERS,data=json.dumps(OPENAI_DATA))
print(response.json()['output'][1]['content'][0]['text'])