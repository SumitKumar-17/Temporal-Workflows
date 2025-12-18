from datetime import timedelta
from temporalio import workflow

# Import activities
with workflow.unsafe.imports_passed_through():
    from activities import delete_milvus, delete_s3, delete_postgres, send_email

@workflow.defn
class DeleteUserWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> list:
        results = []
        
        r1 = await workflow.execute_activity(
            delete_milvus,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )
        results.append(r1)
        
        r2 = await workflow.execute_activity(
            delete_s3,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )
        results.append(r2)
        
        r3 = await workflow.execute_activity(
            delete_postgres,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )
        results.append(r3)
        
        r4 = await workflow.execute_activity(
            send_email,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )
        results.append(r4)
        
        return results
