import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt4(question: str, context: str, prompt_template: str) -> str:
    prompt = prompt_template.format(context=context, question=question)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response["choices"][0]["message"]["content"].strip()