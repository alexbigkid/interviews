"""Unit tests for ingredients.py"""

# Standard library imports
from io import StringIO
import unittest
from unittest.mock import patch

# Third party imports
from parameterized import parameterized

# Local application imports
from context import IngredientsInput

class TestIngredientsInput(unittest.TestCase):

    def setUp(self):
        self.__ingredients_input = IngredientsInput()


    # -------------------------------------------------------------------------
    # Tests for ask_for_ingredients
    # -------------------------------------------------------------------------
    def test_ask_for_ingredients_prompts_user_to_enter_ingredients(self):
        """
            ask_for_ingredients prompts user to enter ingredients
        """
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.__ingredients_input.ask_for_ingredients()
            actual_stdout = fakeOutput.getvalue().rstrip('\n')
            self.assertEqual(actual_stdout, self.__ingredients_input.USER_PROMPT_FOR_INGREDIENTS)


    # -------------------------------------------------------------------------
    # Tests for read_input
    # -------------------------------------------------------------------------
    @parameterized.expand([
        ['eggs', ['eggs']],
        ['Champignon, green apple', ['Champignon', 'green apple']],
        ['green onion, red potatos', ['green onion', 'red potatos']],
        ['green onion, red potatos, sweet potato, dark chocolate',
            ['green onion', 'red potatos', 'sweet potato', 'dark chocolate']],
    ])
    def test_read_input_with_valid_values(self, input, expected):
        """
            read_input is able to read input with valid values
        """
        with patch('builtins.input', return_value=input):
            actual_input = self.__ingredients_input.read_input()
            self.assertEqual(actual_input, expected)


    @parameterized.expand([
        [',OneEgg,', ['OneEgg']],
        [',,TwoEggs', ['TwoEggs']],
        ['ThreeEggs,,', ['ThreeEggs']],
        [',,FourEggs,,', ['FourEggs']],
        [' , , FiveEggs , , ', ['FiveEggs']],
        ['Champignon,, banana', ['Champignon', 'banana']],
        [',, basil , , potatos,,', ['basil', 'potatos']],
    ])
    def test_read_input_should_sanitize_values(self, input, expected):
        """
            read_input can sanitize users input
        """
        with patch('builtins.input', return_value=input):
            actual_input = self.__ingredients_input.read_input()
            self.assertEqual(actual_input, expected)


    @parameterized.expand([
        [''],
        [','],
        [',,'],
        [' ,  , ,'],
        ['42'],
        ['😀'],
        ['😎, 🥸'],
    ])
    def test_read_input_should_throw_exception_given_invalid_input(self, input):
        """
            read_input throws exception
            given user enters invalid characters
        """
        with patch('builtins.input', return_value=input):
            with self.assertRaises(Exception) as exception_message:
                self.__ingredients_input.read_input()
            self.assertEqual(str(exception_message.exception), self.__ingredients_input.INVALID_INPUT_EXCEPTION_MESSAGE)


if __name__ == '__main__':
    unittest.main()
