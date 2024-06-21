import json
import boto3
import os
from uuid import uuid4
from datetime import datetime


dynamodb = boto3.client("dynamodb")
sns_client = boto3.client("sns")
lambda_client = boto3.client("lambda")


TABLE_NAME = os.environ["DYNAMODB_TABLE"]
SYN_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
ASYNC_JOB_FUNC_NAME = os.environ["ASYNC_JOB_FUNC_NAME"]


def service_handler(event, context):
    body = json.loads(event["body"])

    delay = body.get("delay", 0)
    try:
        response = dynamodb.scan(
            TableName=TABLE_NAME,
            FilterExpression="Status = :status",
            ExpressionAttributeValues={":status": {"S": "ACTIVE"}},
        )

        active_jobs = len(response)
        job_limit = 5  # this can be switched to env variables.
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
                "Status": {"S": "ACTIVE"},
                "Timestamp": {"S": datetime.utcnow().isoformat()},
            },
        )

        lambda_client.invoke(
            FunctionName=ASYNC_JOB_FUNC_NAME,
            InvocationType="Event",  # Asynchronous invocation
            Payload=json.dumps({"id": id_param, "delay": delay}),
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
