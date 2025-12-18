from datetime import timedelta
from temporalio import workflow

# Import activities
with workflow.unsafe.imports_passed_through():
    from activities import delete_milvus, delete_s3, delete_postgres, send_email

@workflow.defn
class DeleteMilvusWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> str:
        return await workflow.execute_activity(
            delete_milvus,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )

@workflow.defn
class DeleteS3Workflow:
    @workflow.run
    async def run(self, user_id: str) -> str:
        return await workflow.execute_activity(
            delete_s3,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )

@workflow.defn
class DeletePostgresWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> str:
        return await workflow.execute_activity(
            delete_postgres,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )

@workflow.defn
class SendEmailWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> str:
        return await workflow.execute_activity(
            send_email,
            user_id,
            start_to_close_timeout=timedelta(seconds=60)
        )

@workflow.defn
class DeleteUserWorkflow:
    @workflow.run
    async def run(self, user_id: str) -> list:
        results = []
        
        # Start Deletion Child Workflows in Parallel
        handle1 = await workflow.start_child_workflow(
            DeleteMilvusWorkflow.run,
            user_id,
            id=f"delete-milvus-{user_id}"
        )
        
        handle2 = await workflow.start_child_workflow(
            DeleteS3Workflow.run,
            user_id,
            id=f"delete-s3-{user_id}"
        )
        
        handle3 = await workflow.start_child_workflow(
            DeletePostgresWorkflow.run,
            user_id,
            id=f"delete-postgres-{user_id}"
        )
        
        # Wait for all deletions to complete
        r1 = await handle1
        results.append(r1)
        
        r2 = await handle2
        results.append(r2)
        
        r3 = await handle3
        results.append(r3)
        
        # After all deletions are done, send email
        handle4 = await workflow.start_child_workflow(
            SendEmailWorkflow.run,
            user_id,
            id=f"send-email-{user_id}"
        )
        r4 = await handle4
        results.append(r4)
        
        return results
