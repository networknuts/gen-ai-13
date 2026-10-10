from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="cat"
)
print(response.data[0].embedding)