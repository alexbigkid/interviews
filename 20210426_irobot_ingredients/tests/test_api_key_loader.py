"""Unit tests for shopping_list.py"""

# Standard library imports
import os
import unittest
from unittest.mock import patch, mock_open

# Third party imports

# Local application imports
from context import ApiKeyLoader


class TestApiKeyLoader(unittest.TestCase):


    def setUp(self):
        self.__api_key_loader = ApiKeyLoader()


    # -------------------------------------------------------------------------
    # Tests for get_api_key
    # -------------------------------------------------------------------------
    @patch.dict(os.environ, {'SPOONACULAR_API_KEY': ''})
    def test_get_api_key_throws_given_environment_variable_could_not_be_loaded(self):
        """
            get_api_key throws exception
            given environment variable could not be loaded
        """
        with patch("builtins.open", mock_open(read_data='ABK_TEST_ENV_VAR=[invalid_api_key]')) as mock_file:
            actual_environment_var_value = ''
            with self.assertRaises(Exception) as exception_message:

                actual_environment_var_value = self.__api_key_loader.get_api_key()

            self.assertEqual(str(exception_message.exception), self.__api_key_loader.API_KEY_NOT_FOUND_EXCEPTION_MESSAGE)
            mock_file.assert_called_with(self.__api_key_loader.ENVIRONMENT_FILE_NAME, 'r')
            self.assertEqual(os.environ[self.__api_key_loader.SPOONACULAR_API_KEY], '')
            self.assertEqual(actual_environment_var_value, '')


    @patch.dict(os.environ, {'SPOONACULAR_API_KEY': '[valid_api_key]'})
    def test_get_api_key_returns_from_environment_variable(self):
        """
            get_api_key returns SPOONACULAR_API_KEY value from the environment variable if set
        """
        actual_environment_var_value = ''

        actual_environment_var_value = self.__api_key_loader.get_api_key()

        self.assertEqual(os.environ[self.__api_key_loader.SPOONACULAR_API_KEY], '[valid_api_key]')
        self.assertEqual(actual_environment_var_value, '[valid_api_key]')


    @patch.dict(os.environ, {'SPOONACULAR_API_KEY': ''})
    def test_get_api_key_returns_from_environment_file(self):
        """
            get_api_key returns SPOONACULAR_API_KEY value from .env file
        """
        with patch("builtins.open", mock_open(read_data='SPOONACULAR_API_KEY=[valid_api_key]')) as mock_file:
            actual_environment_var_value = ''

            actual_environment_var_value = self.__api_key_loader.get_api_key()

            mock_file.assert_called_with(self.__api_key_loader.ENVIRONMENT_FILE_NAME, 'r')
            self.assertEqual(os.environ[self.__api_key_loader.SPOONACULAR_API_KEY], '[valid_api_key]')
            self.assertEqual(actual_environment_var_value, '[valid_api_key]')


if __name__ == '__main__':
    unittest.main()
