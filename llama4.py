import requests

OLLAMA_URL = "http://127.0.0.1:11434"

# OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# Define the request payload
payload = {
    "model": "qwen2.5",
    "prompt": "who is ceo of google inc?",
    "stream": False  # Set to True for streaming responses
}

# Send request
response = requests.post(OLLAMA_URL, json=payload)

# Print the response
print(response.json()["response"])