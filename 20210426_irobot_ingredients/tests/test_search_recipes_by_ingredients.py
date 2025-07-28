"""Unit tests for search_recipes_by_ingredients.py"""

# Standard library imports
import os
import unittest
from unittest.mock import patch, mock_open

# Third party imports

# Local application imports
from context import SearchRecipesByIngredients


class TestSearchRecipesByIngredients(unittest.TestCase):
    INGREDIENTS = ['granadilla', 'tomate de arbol', 'lulo', 'maracuya', 'guanabana']
    REQUEST_URL = 'https://api.spoonacular.com/recipes/findByIngredients?ingredients=granadilla,+tomate%20de%20arbol,+lulo,+maracuya,+guanabana&number=8&limitLicense=true&ranking=1&ignorePantry=true&apiKey=[valid_api_key]'
    VALID_JSON_DATA = [{'key1': 'value1'}, {'key2': 'value2'}]
    INVALID_JSON_DATA = []
    JSON_DATA_NOT_CHANGED = [{'data': 'did not change'}]

    def setUp(self):
        self.__search_recipes = SearchRecipesByIngredients()


    # -------------------------------------------------------------------------
    # Tests for get_recipes
    # -------------------------------------------------------------------------
    @patch.dict(os.environ, {'SPOONACULAR_API_KEY': '[valid_api_key]'})
    def test_get_recipes_should_throw_given_response_not_ok_and_json_data_invalid(self):
        """
            get_recipes throws an exception
            given response is not ok and json_data is invalid
        """
        with patch('src.search_recipes_by_ingredients.requests.get') as mock_get:
            actual_response = self.JSON_DATA_NOT_CHANGED
            mock_get.return_value.ok = False
            mock_get.return_value.json.return_value = self.INVALID_JSON_DATA
            with self.assertRaises(Exception) as exception_message:

                actual_response = self.__search_recipes.get_recipes(self.INGREDIENTS)

            self.assertEqual(str(exception_message.exception), self.__search_recipes.INVALID_RESPONSE_EXCEPTION_MESSAGE)
            mock_get.assert_called_with(self.REQUEST_URL)
            self.assertEqual(actual_response, self.JSON_DATA_NOT_CHANGED)


    @patch.dict(os.environ, {'SPOONACULAR_API_KEY': '[valid_api_key]'})
    def test_get_recipes_should_throw_given_response_ok_but_json_data_invalid(self):
        """
            get_recipes throws an exception
            given response is ok, but json_data is invalid
        """
        with patch('src.search_recipes_by_ingredients.requests.get') as mock_get:
            actual_response = self.JSON_DATA_NOT_CHANGED
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = self.INVALID_JSON_DATA
            with self.assertRaises(Exception) as exception_message:

                actual_response = self.__search_recipes.get_recipes(self.INGREDIENTS)

            self.assertEqual(str(exception_message.exception), self.__search_recipes.NO_RECIPES_FOUND_PLEASE_TRY_AGAIN_EXCEPTION_MESSAGE)
            mock_get.assert_called_with(self.REQUEST_URL)
            self.assertEqual(actual_response, self.JSON_DATA_NOT_CHANGED)


    @patch.dict(os.environ, {'SPOONACULAR_API_KEY': '[valid_api_key]'})
    def test_get_recipes_should_throw_given_valid_json_but_response_not_ok(self):
        """
            get_recipes throws an exception
            given response is not ok and json_data is valid
        """
        with patch('src.search_recipes_by_ingredients.requests.get') as mock_get:
            actual_response = self.JSON_DATA_NOT_CHANGED
            mock_get.return_value.ok = False
            mock_get.return_value.json.return_value = self.VALID_JSON_DATA
            with self.assertRaises(Exception) as exception_message:

                actual_response = self.__search_recipes.get_recipes(self.INGREDIENTS)

            self.assertEqual(str(exception_message.exception), self.__search_recipes.INVALID_RESPONSE_EXCEPTION_MESSAGE)
            mock_get.assert_called_with(self.REQUEST_URL)
            self.assertEqual(actual_response, self.JSON_DATA_NOT_CHANGED)


    @patch.dict(os.environ, {'SPOONACULAR_API_KEY': '[valid_api_key]'})
    def test_get_recipes_should_return_valid_data_given_response_ok_and_json_data_valid(self):
        """
            get_recipes should return valid data
            given response is ok and json_data is valid
        """
        with patch('src.search_recipes_by_ingredients.requests.get') as mock_get:
            actual_response = self.JSON_DATA_NOT_CHANGED
            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = self.VALID_JSON_DATA

            actual_response = self.__search_recipes.get_recipes(self.INGREDIENTS)

            mock_get.assert_called_with(self.REQUEST_URL)
            self.assertEqual(actual_response, self.VALID_JSON_DATA)


if __name__ == '__main__':
    unittest.main()
