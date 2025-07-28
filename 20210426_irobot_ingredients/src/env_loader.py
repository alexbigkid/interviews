"""Loades environment variables from a file and reads the value of environment variable"""

# Standard library imports
import os

class EnvLoader():


    def get_environment_variable_value(self, env_variable: str):
        if env_variable in os.environ:
            return os.environ[env_variable]
        else:
            return ''


    def set_environment_varaibales_from_file(self, env_file_with_path: str):
        with open(env_file_with_path, 'r') as file_handle:
            env_variables_dict = dict(
                tuple(line.replace('\n','').split('='))
                for line in file_handle.readlines() if not line.startswith('#')
            )
            # print(env_variables_dict)
            if len(env_variables_dict) > 0:
                os.environ.update(env_variables_dict)
