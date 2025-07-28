"""Unit tests for env_loader.py"""

# Standard library imports
import os
# from unittest import TestCase, mock
import unittest
from unittest.mock import patch, mock_open

# Local application imports
from context import EnvLoader


class TestEnvLoader(unittest.TestCase):

    def setUp(self):
        self.__env_loader = EnvLoader()

    # -------------------------------------------------------------------------
    # Tests for get_environment_variable_value_
    # -------------------------------------------------------------------------
    @patch.dict(os.environ, {'ABK_TEST_ENV_VAR': '[fake_api_key]'})
    def test_get_environment_variable_value_returns_valid_value(self):
        """
            get_environment_variable_value returns a value from the set environment variable
        """
        actual_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
        self.assertEqual(actual_value, '[fake_api_key]')


    @patch.dict(os.environ, {'ABK_TEST_ENV_VAR': ''})
    def test_get_environment_variable_value_should_return_empty_given_env_var_value_is_empty(self):
        """
            get_environment_variable_value returns empty string
            given environment variable is set to empty string
        """
        actual_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
        self.assertEqual(actual_value, '')


    def test_get_environment_variable_value_should_return_empty_given_env_var_undefined(self):
        """
            get_environment_variable_value returns empty string
            given environment variable is not set
        """
        actual_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
        self.assertEqual(actual_value, '')


    # -------------------------------------------------------------------------
    # Tests for set_environment_varaibales_from_file
    # -------------------------------------------------------------------------
    def test_set_environment_varaibales_from_file_sets_one_env_variable(self):
        """
            set_environment_varaibales_from_file sets environment variable read from file
        """
        env_var_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
        self.assertEqual(env_var_value, '')
        with patch("builtins.open", mock_open(read_data='ABK_TEST_ENV_VAR=[fake_api_key]')) as mock_file:

            self.__env_loader.set_environment_varaibales_from_file('does_not_matter')

            env_var_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
            self.assertEqual(env_var_value, '[fake_api_key]')
            mock_file.assert_called_with('does_not_matter', 'r')


    def test_set_environment_varaibales_from_file_sets_several_env_variables(self):
        """
            set_environment_varaibales_from_file sets several environment variables
            after reading from file
        """
        env_var_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR1')
        self.assertEqual(env_var_value, '')
        env_var_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR2')
        self.assertEqual(env_var_value, '')
        data_to_read = 'ABK_TEST_ENV_VAR1=[que_chimba]\nABK_TEST_ENV_VAR2=[no_dar_papaya]'
        with patch("builtins.open", mock_open(read_data=data_to_read)) as mock_file:

            self.__env_loader.set_environment_varaibales_from_file('does_not_matter')

            env_var_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR1')
            self.assertEqual(env_var_value, '[que_chimba]')
            env_var_value = self.__env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR2')
            self.assertEqual(env_var_value, '[no_dar_papaya]')
            mock_file.assert_called_with('does_not_matter', 'r')


    # 1. test cases is missing / not handled if the mal formatted: 'VAR_NAME = VAR_VALUE' not handles spaces
    # def test_set_environment_varaibales_from_file_sets_env_variable_given_line_is_with_white_spaces(self):
    #     env_var_value = self.env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
    #     self.assertEqual(env_var_value, '')
    #     with patch("builtins.open", mock_open(read_data='ABK_TEST_ENV_VAR = [it_is_very_late]')) as mock_file:

    #         self.env_loader.set_environment_varaibales_from_file('does_not_matter')

    #         env_var_value = self.env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
    #         self.assertEqual(env_var_value, '[it_is_very_late]')
            # mock_file.assert_called_with('does_not_matter', 'r')


    # 2. test cases is missing / not handled if the '=' is missing
    # def test_set_environment_varaibales_from_file_does_not_set_env_variable_given_no_value_in_file(self):
    #     env_var_value = self.env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
    #     self.assertEqual(env_var_value, '')
    #     with patch("builtins.open", mock_open(read_data='ABK_TEST_ENV_VAR')) as mock_file:

    #         self.env_loader.set_environment_varaibales_from_file('does_not_matter')

    #         env_var_value = self.env_loader.get_environment_variable_value('ABK_TEST_ENV_VAR')
    #         self.assertEqual(env_var_value, '')
            # mock_file.assert_called_with('does_not_matter', 'r')


    # 3. test case - file does not exist



if __name__ == '__main__':
    unittest.main()
