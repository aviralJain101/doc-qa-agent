import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file from the parent directory
load_dotenv(dotenv_path='.env') 

# Set your Groq API key here or use environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Recommended way
client = OpenAI(base_url="https://api.groq.com/openai/v1",api_key=GROQ_API_KEY)

# TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url="https://api.groq.com/openai/v1")'
# openai.api_base = "https://api.groq.com/openai/v1"

def ask_groq(question: str, context: str, prompt_template: str) -> str:
    prompt = prompt_template.format(context=context, question=question)

    response = client.chat.completions.create(model="llama3-8b-8192",  # You can also use "mixtral-8x7b-32768" if you want
    messages=[
        {"role": "system", "content": "You are a helpful assistant. Be concise and accurate."},
        {"role": "user", "content": prompt},
    ],
    temperature=0.7,
    top_p=0.8,
    max_tokens=1024)

    answer = response.choices[0].message.content
    return answer.strip()