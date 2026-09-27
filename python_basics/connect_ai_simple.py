from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("MY_OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-6-luna",
    input="what is the recipe to make some black coffee?"
)
print(response.output_text)