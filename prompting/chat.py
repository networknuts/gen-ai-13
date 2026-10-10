from dotenv import load_dotenv
from openai import OpenAI

# SYSTEM INSTRUCTIONS
system_instructions = """
you are a devops ai assistant.
you will only answer devops related questions.
if you receive a non-devops question, refuse to answer
that request.
"""

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