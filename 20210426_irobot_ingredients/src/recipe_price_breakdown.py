"""Gets the price breakdown using the Spoonacular API."""

# Standard library imports

# Third party imports
from colorama import Fore, Style
import requests
import json

# Local application imports
from api_key_loader import ApiKeyLoader


class RecipePriceBreakdown():
    INVALID_NUMBER_OF_RECIPES_PASSED_IN = 'No recipe selected to show in the shopping list'
    RECIPE_ID_KEY = 'id'
    RECIPE_TITTLE_KEY = 'title'
    SPOONACULAR_PRICE_BREAKDOWN_API_URL = 'https://api.spoonacular.com/recipes'
    SPOONACULAR_PRICE_BREAKDOWN_API_JSON = 'priceBreakdownWidget.json'
    API_KEY = 'apiKey'                  # API key is the authentication to use to run the get http request. the value must be kept secret


    def __init__(self, liked_recipe_list):
        # protect module from invalid input in case it is taken out of this package
        # and used somewhere else
        if not len(liked_recipe_list) > 0:
            raise Exception(self.INVALID_NUMBER_OF_RECIPES_PASSED_IN)
        self.__liked_recipe_list = liked_recipe_list
        self.__price_list = []
        self.__api_key = ''


    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def get_price_breakdown(self):
        # TODO: This can be improved by sending multiple requests at the same time using multi cores / multi threading
        for liked_recipe in self.__liked_recipe_list:
            request_string = self.__create_request(liked_recipe[self.RECIPE_ID_KEY])
            response = self.__send_request(request_string)
            if self.__is_response_valid(response):
                response_json = response.json()
                response_json[self.RECIPE_ID_KEY] = liked_recipe[self.RECIPE_ID_KEY]
                self.__price_list.append(response_json)
            else:
                # some error happenned here, but we should not raise an exception and terminate the app
                # because the next recipe price request might be ok.
                # Just warning for the user that the price info for this recipe is not available
                print(Fore.YELLOW
                    + f"WARNING: Price information is unavailable for following recipe: "
                    + liked_recipe[self.RECIPE_TITTLE_KEY]
                    + f"{Style.RESET_ALL}"
                )
        return self.__price_list


    # -------------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------------
    def __create_request(self, id):
        api_key_value   = self.__get_api_key()
        req_api_key     = '='.join([self.API_KEY, api_key_value])
        req_url         = '/'.join([self.SPOONACULAR_PRICE_BREAKDOWN_API_URL, str(id), self.SPOONACULAR_PRICE_BREAKDOWN_API_JSON])
        request_string  = '?'.join([req_url, req_api_key])
        # print(request_string)
        return request_string


    def __send_request(self, request_string):
        response = requests.get(request_string)
        # self.__print_json_list(response.json())
        # print(response.text)
        return response


    def __get_api_key(self):
        if self.__api_key:
            return self.__api_key
        api_key_loader = ApiKeyLoader()
        self.__api_key = api_key_loader.get_api_key()
        return self.__api_key


    def __is_response_valid(self, response):
        return response.ok and response.json()


    # def __print_json_list(self, json_data):
    #     ''' This method is not tested since it used for debug info only '''
    #     print('----------------------------------------------------')
    #     print('\n'.join([json.dumps(json_data, indent=2)]))
