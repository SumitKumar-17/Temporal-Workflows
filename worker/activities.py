from temporalio import activity
import asyncio

@activity.defn
async def delete_milvus(user_id: str) -> str:
    print(f"Deleting Milvus data for {user_id}...")
    await asyncio.sleep(5)
    return f"Milvus data deleted for {user_id}"

@activity.defn
async def delete_s3(user_id: str) -> str:
    print(f"Deleting S3 data for {user_id}...")
    await asyncio.sleep(5)
    return f"S3 data deleted for {user_id}"

@activity.defn
async def delete_postgres(user_id: str) -> str:
    print(f"Cascading Deleting Postgres data for {user_id}...")
    await asyncio.sleep(5)
    return f"Postgres data deleted for {user_id}"

@activity.defn
async def send_email(user_id: str) -> str:
    print(f"Sending confirmation email to {user_id}...")
    await asyncio.sleep(5)
    return f"Email sent to {user_id}"
