"""Provides lambda functionality in GL cloud infrastructure"""

# Standard imports
import json
import logging
import os
import sys
from enum import Enum

# 3rd party imports
from jsonschema import validate

# local imports
sys.path.append(os.path.join(os.path.dirname(__file__)))
from gl_hello_io import AhLambdaRequestBody, AhLambdaResponseBody

# -----------------------------------------------------------------------------
# variables definitions, file wide access, for lambda to load only once.
# The values stay loaded in the memory, also some time after lambda execution
# This will accelerate warm start of lambda
# -----------------------------------------------------------------------------
logging.basicConfig()
gl_logger = logging.getLogger(__name__)
log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()
gl_logger.setLevel(logging.getLevelName(log_level))


LAMBDA_RESP_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
    "Content-Type": "application/json",
}

LAMBDA_REQ_SCHEMA = {
    "title": "GL Lambda Request Validation",
    "description": "JSON Schema validation for GL hello get Lambda Request.",
    "$defs": {
        "uuid": {"type": "string", "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", "minLength": 36, "maxLength": 36}
    },

    "type": "object",
    "properties": {
        "deviceUuid":   {"$ref": "#/$defs/uuid"},
        "txId":         {"type": "string", "minLength": 1, "maxLength": 36}
    },
    "required": [
        "deviceUuid",
        "txId"
    ],
    "additionalProperties": False
}

class HttpStatusCode(Enum):
    """HTTP status codes used in this lambda"""
    OK = 200
    FORBIDDEN = 403
    CONFLICT = 409


# -----------------------------------------------------------------------------
# local functions
# -----------------------------------------------------------------------------
def validate_input(input_parameters:dict) -> AhLambdaRequestBody:
    """Validates and converts input parameters
    Args:
        input_parameters (dict[str, str]): lambda input parameter dict
    Raises:
        ValueError: when unexpected values found
    Returns:
        LambdaRequest: converted input_parameters to LambdaRequest
    """
    validate(input_parameters, LAMBDA_REQ_SCHEMA)
    return AhLambdaRequestBody(**input_parameters)


def get_error_response_body(event_body:dict = None) -> AhLambdaResponseBody:
    """Constructs lambda response body in error case
    Args:
        event_body (dict): lambda event body, can be None for GET requests
    Returns:
        LambdaResponseBody: body response
    """
    gl_logger.info(f"-> get_error_response_body()")
    tx_id = ""
    if event_body and isinstance(event_body, dict):
        tx_id = event_body.get('txId', '')
    
    resp_body = AhLambdaResponseBody(
        msg="error",
        txId=tx_id
    )
    gl_logger.info(f"<- get_error_response_body({json.dumps(resp_body._asdict(), indent=4)})")
    return resp_body


def class_to_dict(named_tuple) -> object:
    """ Converts data class or NamedTuple object to dict recursively.
    Args:
        named_tuple: named tuple
    Returns:
        dict: named tuple as dict
    """
    if isinstance(named_tuple, tuple) and hasattr(named_tuple, "_asdict"):
        return {k: class_to_dict(v) for k, v in named_tuple._asdict().items()}
    if isinstance(named_tuple, list):
        return [class_to_dict(v) for v in named_tuple]
    if isinstance(named_tuple, dict):
        return {k: class_to_dict(v) for k, v in named_tuple.items()}
    return named_tuple



# -----------------------------------------------------------------------------
# lambda handler - main function
# -----------------------------------------------------------------------------
def handler(event, context):
    """Handler for removing device from the GL device table.
    Args:
        event (dict): event data dictionary
        context (object): lambda context object
    Returns:
        http_resp dict: lambda response dictionary, where body is a string converted from dict
    """
    status_code = HttpStatusCode.FORBIDDEN.value # Assume error at the beginning, overwrite alter
    gl_logger.info(f"event   = {json.dumps(event, indent=2)}")
    gl_logger.debug(f"context = {json.dumps(context, default=lambda o: getattr(o, '__dict__', str(o)))}")
    resp_body: AhLambdaResponseBody

    try:
        # Handle GET requests without body (for simple hello endpoint)
        if event.get('httpMethod') == 'GET' and not event.get('body'):
            resp_body = AhLambdaResponseBody(
                msg="Hello from GL Lambda!",
                txId="demo-tx-id",
            )
            status_code = HttpStatusCode.OK.value
        else:
            # Handle POST requests with JSON body
            lambda_input = json.loads(event.get('body'))
            lambda_req = validate_input(lambda_input)
            gl_logger.debug(f"req: {json.dumps(lambda_req._asdict(), indent=4)}")

            resp_body = AhLambdaResponseBody(
                msg="ok",
                txId=lambda_req.txId,
            )
            status_code = HttpStatusCode.OK.value
    except Exception as exc:
        gl_logger.error(f"{exc = }")
        try:
            parsed_body = json.loads(event.get('body')) if event.get('body') else None
            resp_body = get_error_response_body(parsed_body)
        except:
            resp_body = get_error_response_body(None)

    body = json.dumps(class_to_dict(resp_body))
    gl_logger.info(f"{status_code = }, {body = }")
    return {"statusCode": status_code, "headers": LAMBDA_RESP_HEADERS, "body": body}
