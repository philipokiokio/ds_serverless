import json
import boto3
import os
from uuid import uuid4
from datetime import datetime


dynamodb = boto3.client("dynamodb")
lambda_client = boto3.client("lambda")


TABLE_NAME = os.environ["DYNAMODB_TABLE"]
ASYNC_JOB_FUNC_NAME = os.environ["ASYNC_JOB_FUNC_NAME"]


def service_handler(event, context):
    body = json.loads(event["body"])

    delay = body.get("delay")
    if delay is None:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"error": "payload sent is unexpected, expects: {'delay': int}"}
            ),
        }

    try:
        """
        If the job is limited to 5 people the approach would include 
        1. The user_uid: this can be extracted via the auth token.
        2. The user_uid is store with every job record in dynamo db with the user_uid. 
        3. This user_uid is then used to query the record of active job as such the filter case is user_uid== user_uid AND status=="ACTIVE"
        4. This case above combine assures that it is impossible to have more than 5 when combine with the rest of the architecture.
        """



        response = dynamodb.scan(
            TableName=TABLE_NAME,
            FilterExpression="JobStatus = :job_status",
            ExpressionAttributeValues={":job_status": {"S": "ACTIVE"}},
        )

        active_jobs = len(response)
        job_limit = 5
        if active_jobs >= job_limit:
            return {
                "statusCode": 429,
                "body": json.dumps(
                    {"message": "Too many concurrent requests. Try again later."}
                ),
            }

        id_param = str(uuid4())
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "IdParam": {"S": id_param},
                "JobStatus": {"S": "ACTIVE"},
                "Timestamp": {"S": datetime.utcnow().isoformat()},
            },
        )
        body = json.dumps({"body": json.dumps({"id": id_param, "delay": delay})})
        lambda_client.invoke(
            FunctionName=ASYNC_JOB_FUNC_NAME,
            InvocationType="Event",
            Payload=body,
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Job submitted successfully"}),
        }
    except Exception:

        return {
            "statusCode": 500,
            "body": json.dumps({"error": "something went wrong"}),
        }
