from dotenv import load_dotenv
from openai import OpenAI

# SYSTEM INSTRUCTIONS
f = open("few_shot_prompt.txt","r")
system_instructions = f.read()
f.close()

# STEP 1: LOAD THE .ENV FILE
load_dotenv()
query = input("Enter your question: ")

# STEP 2: MAKING THE LLM REQUEST
client = OpenAI()
response = client.responses.create(
    model="gpt-5.6-luna",
    instructions=system_instructions,
    input=query
)

# STEP 3: PRINT RESPONSE
print(response.output_text)