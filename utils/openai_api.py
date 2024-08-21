import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def analyze_text_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"].strip()
