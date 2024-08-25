import openai

# Set the necessary configuration for Azure OpenAI
openai.api_type = "azure"
openai.api_key = "aa4f2f35c7634fcb8f5b652bbfb36926"
openai.api_base = "https://nw-tech-dev.openai.azure.com/"
openai.api_version = "2023-03-15-preview"

# Set your deployment ID here
deployment_id = "gpt-4o"  # Replace with your actual deployment ID

def analyze_text_with_openai(prompt):
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        deployment_id=deployment_id,
        messages=messages,
    )

    return response.choices[0].message["content"].strip()
