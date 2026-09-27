import requests
import os
import json
from dotenv import load_dotenv
from ai_function import talk_to_ai

load_dotenv()
my_ai_response = talk_to_ai("what is the capital of india?","aryan srivastava")
print(my_ai_response)