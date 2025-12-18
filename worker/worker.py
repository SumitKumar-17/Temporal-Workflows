import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import DeleteUserWorkflow
from activities import delete_milvus, delete_s3, delete_postgres, send_email

TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "localhost:7233")

async def main():
    print(f"Connecting to Temporal at {TEMPORAL_HOST}...")
    # Wait for Temporal to be ready
    while True:
        try:
            client = await Client.connect(TEMPORAL_HOST)
            break
        except Exception as e:
            print(f"Waiting for Temporal... {e}")
            await asyncio.sleep(2)

    print("Connected to Temporal. Starting worker...")
    worker = Worker(
        client,
        task_queue="delete-user-task-queue",
        workflows=[DeleteUserWorkflow],
        activities=[delete_milvus, delete_s3, delete_postgres, send_email],
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
