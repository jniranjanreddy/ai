from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# enable cors   
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_API = "http://127.0.0.1:11434"

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    """Send chat request to Qwen via Ollama API"""
    try:
        logger.info(f"Received chat request: {request.message[:100]}...")
        
        # Prepare the request for Ollama chat API
        ollama_request = {
            "model": "qwen2.5",
            "messages": [{"role": "user", "content": request.message}],
            "stream": False
        }
        
        # Send request to Ollama
        response = requests.post(f"{OLLAMA_API}/api/chat", json=ollama_request)
        
        if response.status_code != 200:
            logger.error(f"Ollama API error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=503, detail=f"Qwen service error: {response.text}")
        
        result = response.json()
        logger.info("Successfully received response from Qwen")
        
        return {"response": result["message"]["content"]}
        
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama service")
        raise HTTPException(status_code=503, detail="Cannot connect to Qwen. Please ensure Ollama is running on 127.0.0.1:11434")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
def home():
    return {
        "message": "Qwen Chatbot API is running",
        "endpoints": [
            "GET /",
            "GET /health",
            "GET /debug/models",
            "POST /chat"
        ],
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """Check if Qwen model is available and ready"""
    try:
        # Test connection to Ollama
        response = requests.get(f"{OLLAMA_API}/api/tags")
        
        if response.status_code == 200:
            models = response.json()
            model_list = models.get('models', [])
            
            # Handle different response formats
            qwen_models = []
            all_models = []
            
            for model in model_list:
                if isinstance(model, dict):
                    model_name = model.get('name', '')
                    all_models.append(model_name)
                    if 'qwen' in model_name.lower():
                        qwen_models.append(model_name)
                elif isinstance(model, str):
                    all_models.append(model)
                    if 'qwen' in model.lower():
                        qwen_models.append(model)
            
            if qwen_models:
                return {
                    "status": "healthy",
                    "qwen_available": True,
                    "available_qwen_models": qwen_models,
                    "ollama_url": OLLAMA_API,
                    "message": "Qwen is ready to chat!"
                }
            else:
                return {
                    "status": "unhealthy",
                    "qwen_available": False,
                    "available_models": all_models,
                    "ollama_url": OLLAMA_API,
                    "message": "Qwen model not found. Install with: ollama pull qwen2.5"
                }
        else:
            return {
                "status": "error",
                "qwen_available": False,
                "error": f"Ollama API returned {response.status_code}",
                "ollama_url": OLLAMA_API,
                "message": "Cannot connect to Ollama service"
            }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "error",
            "qwen_available": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "ollama_url": OLLAMA_API,
            "message": "Cannot connect to Ollama service"
        }

@app.get("/debug/models")
async def debug_models():
    """Debug endpoint to see raw Ollama response"""
    try:
        response = requests.get(f"{OLLAMA_API}/api/tags")
        return {
            "status_code": response.status_code,
            "raw_response": response.json() if response.status_code == 200 else response.text,
            "url": f"{OLLAMA_API}/api/tags"
        }
    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "url": f"{OLLAMA_API}/api/tags"
        }