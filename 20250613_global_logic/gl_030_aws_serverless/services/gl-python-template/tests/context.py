"""Test Harness external packages imports"""
import os
import sys

# from unittest.mock import MagicMock
# import boto3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# os.environ['GL_DB_USR']                = '[fake_db_usr]'
# os.environ['GL_DB_PSW']                = '[fake_db_psw]'
# os.environ['GL_DB_HOST']               = '[fake_db_host]'
# os.environ['GL_DB_PORT']               = '8989'
# os.environ['GL_DB_NAME']               = '[fake_db_name]'
# os.environ['GL_DB_NAME']               = '[fake_db_name]'

# mock_iot_client = MagicMock()
# boto3.client = MagicMock(side_effect=[mock_iot_client])

import gl_hello
from gl_hello_io import AhLambdaRequestBody, AhLambdaResponseBody
