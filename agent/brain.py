import os

from dotenv import load_dotenv
from openai import OpenAI
'''
Code	What it does
import os	Allows Python to access environment variables.
load_dotenv	Loads information stored in your .env file.
OpenAI	Provides the client library used to communicate with DeepSeek's compatible API.
load_dotenv()	Reads your .env file.
os.getenv(...)	Retrieves your API key without hardcoding it in Python.
OpenAI(...)	Creates the connection client for DeepSeek.

Important: We are using the OpenAI Python library as a
 communication tool. We are connecting it to DeepSeek 
 through its API address. Your actual API key stays inside .env.

'''

# Load environment variables from .env
load_dotenv()

# Read the DeepSeek API key
api_key = os.getenv("DEEPSEEK_API_KEY")

# Create our DeepSeek client
deepseek_client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

'''
Before we teach our AI to analyse server logs, 
let's understand one important concept: 
How do we send a message to DeepSeek and receive an answer?
Make your first AI call from below function.

'''


SYSTEM_PROMPT = """
You are an experienced Level 1 IT Support Analyst.

Your responsibilities are:

1. Analyse the server health information and log messages provided.
2. Explain what the evidence indicates.
3. Identify possible causes of the incident.
4. Recommend safe troubleshooting steps for a human IT engineer.
5. Never claim an unconfirmed root cause as a fact.
6. Never claim that you have restarted a service or fixed an issue.
7. If the evidence is insufficient, clearly explain what information is missing.
8. Use simple, structured language.
"""


def ask_deepseek(prompt):

    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
           {
            "role": "system",
            "content": SYSTEM_PROMPT
           },
           {
            "role": "user",
            "content": prompt
           }
        ]
    )

    return response.choices[0].message.content