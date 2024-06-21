import json
import os
import boto3


dynamodb = boto3.client("dynamodb")

TABLE_NAME = os.environ["DYNAMODB_TABLE"]


def lambda_handler(event, context):

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
        # TODO SNS Topics Completion
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Job status updated to COMPLETED"}),
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid id parameter"}),
        }
