# Core application API requests with FastAPI from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from rq import Queue
from redis import Redis



# create the core application instance
app = FastAPI()


redis_conn = Redis(host="localhost", port=6379, decode_responses=True)
queue = Queue("chat_jobs", connection=redis_conn)


class ChatRequest(BaseModel):
    message: str

def chat_message(message: str):
    return {"message": f"processed {message}"}

# returns health check response to ensure the server is correctly running
@app.get("/")
def status():
    return {
        "success": True,
        "message": "OK"
    }

# POST /chat accepts JSON as {"message": "hello"} returns {"message": "processed hello"}
@app.post("/chat")
async def create_message(data: ChatRequest):
    job = queue.enqueue(chat_message, data.message)
    return {"job_id": job.id, "status": "queued"}