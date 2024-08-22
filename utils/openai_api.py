import openai

# Set the necessary configuration for Azure OpenAI
openai.api_type = "azure"
openai.api_base = "https://nw-tech-wu.openai.azure.com/"  # Your Azure OpenAI endpoint
openai.api_key = "aa4f2f35c7634fcb8f5b652bbfb36926"  # Your Azure OpenAI API key
openai.api_version = "2024-02-01"  # The API version for Azure OpenAI

# Set your deployment ID here
deployment_id = "gpt-4o"  # Replace with your actual deployment ID

def analyze_text_with_openai(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        engine=deployment_id,  # The deployment ID is used as the engine name
        messages=messages,
    )

    return response['choices'][0]['message']['content'].strip()
