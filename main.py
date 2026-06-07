# Core application API requests with FastAPI from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job
from redis import Redis
from uuid import uuid4


# create the core application instance
app = FastAPI()


redis_conn = Redis(host="localhost", port=6379)
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

def fetch_job(job_id: str) -> Job:
    try:
        return Job.fetch(job_id, connection=redis_conn)
    except NoSuchJobError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = fetch_job(job_id)
    return {
        "job_id": job.id,
        "status": job.get_status(refresh=True).value
    }


@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = fetch_job(job_id)
    status = job.get_status(refresh=True)

    if status.value != "finished":
        return {
            "job_id": job_id,
            "status": status.value
        }

    return {
        "job_id": job_id,
        "status": status.value,
        "response": job.return_value(refresh=True)
    }


# POST /chat accepts JSON as {"message": "hello"} returns {"message": "processed hello"}
@app.post("/chat")
async def create_job(data: ChatRequest):
    job_id = str(uuid4())
    payload = {
        "job_id": job_id,
        "message": data.message
    }
    job = queue.enqueue(
        "services.jobs.process_chat_job",
        payload,
        job_id=job_id
    )
    return {
        "job_id": job.id,
        "status": job.get_status(refresh=False).value
    }
