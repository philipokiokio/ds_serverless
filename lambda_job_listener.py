import json
import os
import boto3


dynamodb = boto3.client("dynamodb")
sns_client = boto3.client("sms")

TABLE_NAME = os.environ["DYNAMODB_TABLE"]
SNS_TOPIC = os.environ["SNS_TOPIC_ARN"]


def job_listener_handler(event, context):

    detail = json.loads(event["detail"])
    id_param = detail.get("id")

    if id_param:
        dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={"IdParam": {"S": id_param}, "Status": {"S": "ACTIVE"}},
            UpdateExpression="SET #status = :completed",
            ExpressionAttributeNames={"#status": "Status"},
            ExpressionAttributeValues={":completed": {"S": "COMPLETED"}},
        )

        message = json.dumps({"message": "Job completed", "id": id_param})
        sns_client.publish(
            TopicArn=SNS_TOPIC, Message=message, Subject="Job Completion Notification"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Job status updated to COMPLETED"}),
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid id parameter"}),
        }
