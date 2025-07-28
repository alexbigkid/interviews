"""Unit tests for gl_hello.py"""

# Standard library imports
import json
import logging
import os
import unittest
import uuid
from datetime import datetime
from typing import Union
from unittest.mock import ANY, call, patch

# Own modules imports
from context import AhLambdaRequestBody, AhLambdaResponseBody, gl_hello
# Third party imports
from parameterized import parameterized

logging.basicConfig(format='[%(funcName)s]:[%(levelname)s]: %(message)s')
tst_logger = logging.getLogger(__name__)
log_level = os.environ.get("LOG_LEVEL", "WARNING").upper()
tst_logger.setLevel(logging.getLevelName(log_level))



# -----------------------------------------------------------------------------
# help classes
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# local constants
# -----------------------------------------------------------------------------
# Common test definitions
# -----------------------------------------------------------------------------
TEST_ST_THING_NAME      = 'abeabeab-eabe-abea-beab-abeabeabeabe'
VALID_REQ = AhLambdaRequestBody(
    deviceUuid=TEST_ST_THING_NAME,
    txId="test_txId_from_valid_lambda_req"
)

INVALID_RESP_BODY = AhLambdaResponseBody(
    msg="error",
    txId=VALID_REQ.txId
)


class TestLambdaResponse():
    """Holds test data for LambdaResponse."""
    def __init__(self, status_code:int, body_str:str):
        self._resp = {
            "statusCode": status_code,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json",
            },
            "body": body_str
        }

    @property
    def resp(self):
        """Returns lambda response"""
        return self._resp


# -----------------------------------------------------------------------------
# class for testing GL lambda
# -----------------------------------------------------------------------------
class TestGlHello(unittest.TestCase):
    """Test for gl_hello"""

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL) # disables logging
        # logging.disable(logging.NOTSET) # enables logging

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)


    def setUp(self) -> None:
        self.maxDiff = None
        self.valid_input = VALID_REQ._asdict()
        return super().setUp()


    # -------------------------------------------------------------------------
    # Tests for LambdaRequest conversion
    # -------------------------------------------------------------------------
    def test_gl_hello__converting_lambda_input_parameters(self) -> None:
        """Validates that the lambda input parameters are converted correctly"""
        actual_req = AhLambdaRequestBody(**self.valid_input)
        # tst_logger.debug(f'actual_req: {json.dumps(actual_req._asdict(), indent=4)}')
        # tst_logger.debug(f'expected_req: {json.dumps(VALID_REQ._asdict(), indent=4)}')
        self.assertEqual(actual_req, VALID_REQ)


    # -------------------------------------------------------------------------
    # Tests for validate_input
    # -------------------------------------------------------------------------
    @parameterized.expand([
        [ 'deviceUuid'  ],
        [ 'txId'        ]
    ])
    def test_convert_and_validate_input__throws_given_required_input_key_missing(self, key_to_delete) -> None:
        """Validates that exception is thrown when one of the required keys is missing"""
        lcl_actual_input = self.valid_input
        del lcl_actual_input[key_to_delete]
        lcl_exception_msg = f"'{key_to_delete}' is a required property"
        with self.assertRaises(Exception) as exception_message:
            gl_hello.validate_input(lcl_actual_input)
        # tst_logger.info(f"{exception_message.exception = }")
        self.assertIn(lcl_exception_msg, str(exception_message.exception))


    def test_convert_and_validate_input__throws_given_additional_input_key_is_present(self) -> None:
        """Validates that exception is thrown when additional keys is present in the lambda request"""
        lcl_actual_input = self.valid_input
        lcl_additional_parameter_key = "additional_parameter_value"
        lcl_actual_input[lcl_additional_parameter_key] = "notAllowed"
        lcl_exception_msg = f"Additional properties are not allowed ('{lcl_additional_parameter_key}' was unexpected)"
        with self.assertRaises(Exception) as exception_message:
            gl_hello.validate_input(lcl_actual_input)
        self.assertIn(lcl_exception_msg, str(exception_message.exception))


    @parameterized.expand([
        # key,          value       exception message
        [ 'deviceUuid', 'aec4f817-0729-442e-bf6b-588b2a2011b60', "'aec4f817-0729-442e-bf6b-588b2a2011b60' does not match" ],
        [ 'deviceUuid', 'NotValid', "'NotValid' does not match"                 ],
        [ 'deviceUuid', '',         "'' does not match"                         ],
        [ 'deviceUuid', True,       "True is not of type 'string'"              ],
        [ 'deviceUuid', 89,         "89 is not of type 'string'"                ],
        [ 'deviceUuid', 3.14,       "3.14 is not of type 'string"               ],
        [ 'deviceUuid', {},         "{} is not of type 'string'"                ],
        [ 'deviceUuid', [],         "[] is not of type 'string'"                ],
        [ 'txId',       '',         "'' is too short"                           ],
        [ 'txId',       'X'*37,     f"\'{'X'*37}\' is too long"                 ],
        [ 'txId',       True,       "True is not of type 'string'"              ],
        [ 'txId',       89,         "89 is not of type 'string'"                ],
        [ 'txId',       3.14,       "3.14 is not of type 'string'"              ],
        [ 'txId',       {},         "{} is not of type 'string'"                ],
        [ 'txId',       [],         "[] is not of type 'string'"                ]
    ])
    def test_convert_and_validate_input__throws_given_invalid_input(self, p_key:str, p_value, ex_msg:str) -> None:
        """Validates exception is thrown when unexpected value is seen"""
        lcl_actual_input = self.valid_input
        lcl_actual_input[p_key] = p_value
        with self.assertRaises(Exception) as exception_message:
            gl_hello.validate_input(lcl_actual_input)
        # tst_logger.info(f"{exception_message.exception = }")
        self.assertIn(ex_msg, str(exception_message.exception))


    # -------------------------------------------------------------------------
    # Helper functions
    # -------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
