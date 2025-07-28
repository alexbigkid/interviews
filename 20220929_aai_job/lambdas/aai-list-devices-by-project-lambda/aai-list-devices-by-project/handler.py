import json

def lambda_handler(event, context):
    body = {
        "message": "Alex is Awesome!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
