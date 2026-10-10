from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-6-luna",
    input="what is the weather today in new york?"
)
print(response.output_text)