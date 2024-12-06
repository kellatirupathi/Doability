import os
import openai
from openai import AzureOpenAI

openai.api_type = "azure"
client = AzureOpenAI(
    # azure_endpoint="https://nw-tech-wu.openai.azure.com/",
    # api_key="fce9b34907b848a6902e5c37ddfc8512",
    # api_version="2024-02-01",
    azure_endpoint="https://nw-tech-dev.openai.azure.com/",
    api_key="aa4f2f35c7634fcb8f5b652bbfb36926",
    api_version="2023-03-15-preview",
)

def analyze_text_with_openai(prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    return response.choices[0].message.content.strip()

# Example usage
prompt = "Tell me about the benefits of using AI in business."
result = analyze_text_with_openai(prompt)
print(result)
