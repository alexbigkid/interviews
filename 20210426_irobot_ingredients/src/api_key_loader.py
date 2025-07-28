"""Loads SPOONACULAR_API_KEY from environment variable or .env file"""

# Local application imports
from env_loader import EnvLoader


class ApiKeyLoader():
    SPOONACULAR_API_KEY = 'SPOONACULAR_API_KEY'
    ENVIRONMENT_FILE_NAME = '.env'
    API_KEY_NOT_FOUND_EXCEPTION_MESSAGE = 'EXCEPTION: spoonacular API key could not be found. Please load env variable {} with api key or set it in the {} file.'.format(SPOONACULAR_API_KEY, ENVIRONMENT_FILE_NAME)


    def get_api_key(self):
        env_loader = EnvLoader()
        spoonacular_api_key = env_loader.get_environment_variable_value(self.SPOONACULAR_API_KEY)
        if not spoonacular_api_key:
            env_loader.set_environment_varaibales_from_file(self.ENVIRONMENT_FILE_NAME)
            spoonacular_api_key = env_loader.get_environment_variable_value(self.SPOONACULAR_API_KEY)
            if not spoonacular_api_key:
                raise Exception(self.API_KEY_NOT_FOUND_EXCEPTION_MESSAGE)
        return spoonacular_api_key
