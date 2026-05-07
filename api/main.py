# Core application API requests with FastAPI from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

# create the core application instance
app = FastAPI()

class ChatRequest(BaseModel):
    message: str

def chat_message(message: str):
    return {"message": f"processed {message}"}

# returns health check response to ensure the server is correctly running
@app.get("/")
async def root():
    return{"message": "API is running"}

# POST /chat accepts JSON as {"message": "hello"} returns {"message": "processed hello"}
@app.post("/chat")
async def create_message(chat: ChatRequest):
    return chat_message(chat.message)