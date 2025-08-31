from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

# Replace with your Azure OpenAI credentials
ENDPOINT = ""
API_KEY = ""
DEPLOYMENT_NAME = ""  # E.g., 'gpt-35-turbo'

# Initialize the client
client = OpenAIClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

# Prompt for the OpenAI model
prompt = "Write a short poem about the Azure cloud."

# Request the completion
response = client.get_completions(
    deployment_id=DEPLOYMENT_NAME,
    prompt=prompt,
    max_tokens=50,
)

# Extract and print the response
for choice in response.choices:
    print(choice.text.strip())
