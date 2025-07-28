"""Lambda In / Out - Request / Response definitions"""
from typing import NamedTuple, Optional


class AhLambdaRequestBody(NamedTuple):
    """Class to store lambda request
    An example of the lambda request would be:
    {
        "deviceUuid": "15a73c3e-0c86-495a-aa2b-522691d93d60",
        "txId": "any_thing_with_length_upto_36_chars",
    }
    """
    deviceUuid: str         # required / should not be empty
    txId: str               # required / should not be empty


class AhLambdaResponseBody(NamedTuple):
    """Class to store lambda response body information
    An example of the lambda response body would be:
    {
        "msg": "OK",
        "txId": "any_thing_with_length_upto_36_chars"
    }
    """
    msg: str
    txId: str


class AhLambdaResponse(NamedTuple):
    """Class to store lambda response
    An example of the lambda response would be:
    {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Content-Type": "application/json",
        },
        "body": json.dumps(lambdaResponseBody)
    }
    """
    statusCode: int
    headers: Optional[dict]
    body: str
