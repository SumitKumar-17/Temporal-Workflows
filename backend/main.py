from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import redis
import os
from temporalio.client import Client

app = FastAPI()

app.mount("/ui", StaticFiles(directory="frontend", html=True), name="ui")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost:7233")

# Retry connection to Redis if needed, but Docker depends_on helps
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

class DeleteRequest(BaseModel):
    user_id: str

@app.post("/delete-request")
async def request_deletion(req: DeleteRequest):
    # Push to Redis
    r.lpush("delete_requests_queue", req.user_id)
    return {"status": "requested", "user_id": req.user_id}

@app.get("/admin/requests")
async def get_requests():
    # Get all requests
    requests = r.lrange("delete_requests_queue", 0, -1)
    return {"requests": requests}

@app.post("/admin/approve")
async def approve_deletion(req: DeleteRequest):
    # Remove from Redis (remove 1 occurrence)
    r.lrem("delete_requests_queue", 1, req.user_id)
    
    # Start Temporal Workflow
    try:
        client = await Client.connect(TEMPORAL_HOST)
        handle = await client.start_workflow(
            "DeleteUserWorkflow",
            req.user_id,
            id=f"delete-user-{req.user_id}",
            task_queue="delete-user-task-queue",
        )
        return {"status": "approved", "workflow_id": handle.id}
    except Exception as e:
        # Put it back if failed? Or just error out.
        # For demo, just error.
        raise HTTPException(status_code=500, detail=str(e))
