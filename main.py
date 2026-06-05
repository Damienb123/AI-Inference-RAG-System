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

# Job status updates and result retrieval 
# Track async jobs
# Example endpoints: GET /status/{job_id} | GET /result/{job_id}
@app.get("/status/{job_id}")
async def get_status(job_id: str):
    result = redis_conn.get(f"result: {job_id}")
    queue.enqueue()

    if result: 
        return {
            "job_id": True,
            "status": "Completed"
        }
    return {
                "job_id": False,
                "status": "Processing"
            }

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    result = redis_conn.get(f"result: {job_id}")
    
    if not result:
        return {
            "job_id": job_id,
            "status": "Processing"
        }
    return {
          "job_id": job_id,
          "status": "Completed",
          "response": result

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
