# Contains the actual job logic therefore to define the job function
def process_chat_job(payload):
    message = payload["message"]
    job_id = payload["job_id"]
    return {"job_id": job_id, "message": f"processed {message}"}