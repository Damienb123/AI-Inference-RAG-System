# Core application API requests with FastAPI from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from rq import Queue
from redis import Redis
from uuid import uuid4

# create the core application instance
app = FastAPI()


redis_conn = Redis(host="localhost", port=6379, decode_responses=True)
queue = Queue("chat_jobs", connection=redis_conn)


class ChatRequest(BaseModel):
    message: str


# returns health check response to ensure the server is correctly running
@app.get("/")
def status():
    return {
        "success": True,
        "message": "OK"

    }

# POST /chat accepts JSON as {"message": "hello"} returns {"message": "processed hello"}
@app.post("/chat")
async def create_job(data: ChatRequest):
    job_id = str(uuid4())
    queue.enqueue("services.jobs.process_chat_job", payload)
    payload = {
        "job_id": job_id,
        "message": data.message
    }
