from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import ollama
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Configure Ollama client
ollama_client = ollama.Client(host="http://127.0.0.1:11434")  # Adjust if needed

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The user message to send to the model")

@app.post("/chat")
async def chat(request: ChatRequest):
    logging.info(f"Received message: {request.message}")
    try:
        response = ollama_client.chat(model="qwen2.5", messages=[{"role": "user", "content": request.message}])
        logging.info(f"Model response: {response}")
        if "message" not in response or "content" not in response["message"]:
            raise HTTPException(status_code=500, detail="Invalid response from model")
        return {"response": response["message"]["content"]}
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Qwen Chatbot API is running"}

@app.get("/health")
async def health():
    try:
        ollama_client.list()
        return {"status": "healthy", "model": "qwen2.5"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")