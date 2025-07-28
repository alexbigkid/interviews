"""Unit tests for recipe_view.py"""

# Standard library imports
from io import StringIO
import unittest
from unittest.mock import patch

# Third party imports

# Local application imports
from context import RecipeView


class TestRecipeView(unittest.TestCase):
    TEST_DATA = [{"id":656323,"title":"Pita Pizzas with Sautéed Apples and Bacon","image":"https://spoonacular.com/recipeImages/656323-312x231.jpg","imageType":"jpg","usedIngredientCount":3,"missedIngredientCount":8,"missedIngredients":[{"id":18413,"amount":2.0,"unit":"","unitLong":"","unitShort":"","aisle":"Bakery/Bread","name":"pitas","original":"2 pitas","originalString":"2 pitas","originalName":"pitas","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/pita-bread.jpg"},{"id":10862,"amount":4.0,"unit":"slices","unitLong":"slices","unitShort":"slice","aisle":"Meat","name":"cooked bacon","original":"4 slices of bacon, cooked and crumbled","originalString":"4 slices of bacon, cooked and crumbled","originalName":"bacon, cooked and crumbled","metaInformation":["crumbled","cooked"],"meta":["crumbled","cooked"],"image":"https://spoonacular.com/cdn/ingredients_100x100/cooked-bacon.jpg"},{"id":10011282,"amount":0.5,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"red onion","original":"1/2 red onion, sliced","originalString":"1/2 red onion, sliced","originalName":"red onion, sliced","metaInformation":["red","sliced"],"meta":["red","sliced"],"image":"https://spoonacular.com/cdn/ingredients_100x100/red-onion.png"},{"id":1001009,"amount":0.75,"unit":"cup","unitLong":"cups","unitShort":"cup","aisle":"Cheese","name":"shredded cheddar cheese","original":"3/4 cup cheddar cheese, shredded","originalString":"3/4 cup cheddar cheese, shredded","originalName":"cheddar cheese, shredded","metaInformation":["shredded"],"meta":["shredded"],"image":"https://spoonacular.com/cdn/ingredients_100x100/shredded-cheddar.jpg"},{"id":2010,"amount":0.5,"unit":"teaspoon","unitLong":"teaspoons","unitShort":"tsp","aisle":"Spices and Seasonings","name":"cinnamon","original":"1/2 teaspoon cinnamon","originalString":"1/2 teaspoon cinnamon","originalName":"cinnamon","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/cinnamon.jpg"},{"id":1002011,"amount":1.0,"unit":"cloves","unitLong":"clove","unitShort":"cloves","aisle":"Spices and Seasonings","name":"cloves","original":"of cloves","originalString":"of cloves","originalName":"of","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/cloves.jpg"},{"id":1032009,"amount":0.75,"unit":"teaspoon","unitLong":"teaspoons","unitShort":"tsp","aisle":"Spices and Seasonings","name":"chili flakes","original":"3/4 teaspoon crushed chili pepper flakes","originalString":"3/4 teaspoon crushed chili pepper flakes","originalName":"crushed chili pepper flakes","metaInformation":["crushed"],"meta":["crushed"],"image":"https://spoonacular.com/cdn/ingredients_100x100/red-pepper-flakes.jpg"},{"id":1001,"amount":1.0,"unit":"tablespoon","unitLong":"tablespoon","unitShort":"Tbsp","aisle":"Milk, Eggs, Other Dairy","name":"butter","original":"1 tablespoon butter","originalString":"1 tablespoon butter","originalName":"butter","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg"}],"usedIngredients":[{"id":1089003,"amount":1.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"granny smith apple","original":"1 granny smith apple, cored and sliced","originalString":"1 granny smith apple, cored and sliced","originalName":"granny smith apple, cored and sliced","metaInformation":["cored","sliced"],"meta":["cored","sliced"],"image":"https://spoonacular.com/cdn/ingredients_100x100/grannysmith-apple.png"},{"id":11215,"amount":4.0,"unit":"cloves","unitLong":"cloves","unitShort":"cloves","aisle":"Produce","name":"garlic","original":"4 cloves of garlic, minced (divided)","originalString":"4 cloves of garlic, minced (divided)","originalName":"garlic, minced (divided)","metaInformation":["divided","minced","()"],"meta":["divided","minced","()"],"image":"https://spoonacular.com/cdn/ingredients_100x100/garlic.png"},{"id":2021,"amount":0.25,"unit":"teaspoon","unitLong":"teaspoons","unitShort":"tsp","aisle":"Spices and Seasonings","name":"ground ginger","original":"1/4 teaspoon ground ginger","originalString":"1/4 teaspoon ground ginger","originalName":"ground ginger","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}],"unusedIngredients":[{"id":11216,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce;Ethnic Foods;Spices and Seasonings","name":"ginger","original":"ginger","originalString":"ginger","originalName":"ginger","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}],"likes":1},{"id":647615,"title":"Huli-Huli Chicken","image":"https://spoonacular.com/recipeImages/647615-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":2,"missedIngredients":[{"id":1005006,"amount":6.0,"unit":"","unitLong":"","unitShort":"","aisle":"Meat","name":"chicken drumsticks and thighs","original":"6 CHICKEN DRUMSTICKS AND 4 THIGHS","originalString":"6 CHICKEN DRUMSTICKS AND 4 THIGHS","originalName":"CHICKEN DRUMSTICKS AND 4 THIGHS","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/chicken-parts.jpg"},{"id":9266,"amount":8.0,"unit":"ounces","unitLong":"ounces","unitShort":"oz","aisle":"Produce","name":"pineapple","original":"8 ounces crushed pineapple, undrained","originalString":"8 ounces crushed pineapple, undrained","originalName":"crushed pineapple, undrained","metaInformation":["crushed","undrained"],"meta":["crushed","undrained"],"image":"https://spoonacular.com/cdn/ingredients_100x100/pineapple.jpg"}],"usedIngredients":[{"id":11215,"amount":4.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"garlic cloves","original":"4 CLOVES GARLIC -SMASHED","originalString":"4 CLOVES GARLIC -SMASHED","originalName":"CLOVES GARLIC -SMASHED","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/garlic.png"},{"id":11216,"amount":4.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce;Ethnic Foods;Spices and Seasonings","name":"ginger root","original":"4 SLICES GINGER ROOT-SMASHED","originalString":"4 SLICES GINGER ROOT-SMASHED","originalName":"SLICES GINGER ROOT-SMASHED","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}],"unusedIngredients":[{"id":1089003,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"granny smith apple","original":"granny smith apple","originalString":"granny smith apple","originalName":"granny smith apple","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/grannysmith-apple.png"}],"likes":2}]
    EXPECTED_RECIPE_OUTPUT_1 = [
        'Number of recipes found matching provided ingredients: 2',
        '================================================================================',
        'Recipe number: 1',
        'Recipe title: Pita Pizzas with Sautéed Apples and Bacon',
        'Your ingredients: granny smith apple, garlic, ground ginger',
        'Additional ingredients: pitas, cooked bacon, red onion, shredded cheddar cheese, cinnamon, cloves, chili flakes, butter',
        '[33mDo you like the recipe? No maybe! Please answer with yes(y) or no(n)',
        'Anything else but "Yes" would be taken as "No"',
        'You answered with:'
    ]
    EXPECTED_RECIPE_OUTPUT_2 = [
        '--------------------------------------------------------------------------------',
        'Recipe number: 2',
        'Recipe title: Huli-Huli Chicken',
        'Your ingredients: garlic cloves, ginger root',
        'Additional ingredients: chicken drumsticks and thighs, pineapple',
        '[33mDo you like the recipe? No maybe! Please answer with yes(y) or no(n)',
        'Anything else but "Yes" would be taken as "No"',
        'You answered with:'
    ]


    def setUp(self):
        self.__recipe_view = RecipeView(self.TEST_DATA)


    # -------------------------------------------------------------------------
    # Tests for constructor
    # -------------------------------------------------------------------------
    def test_recipe_view_constructor_should_throw_given_empty_list_passed_in(self):
        """
            the constructor should throw an exception
            when invalid / empty list is passed in
        """
        with self.assertRaises(Exception) as exception_message:
            self.__recipe_view = RecipeView([])
        self.assertEqual(str(exception_message.exception), self.__recipe_view.INVALID_NUMBER_OF_RECIPES_PASSED_IN)


    # -------------------------------------------------------------------------
    # Tests for show_recipe_list and get_liked_recipe_list
    # -------------------------------------------------------------------------
    def test_show_recipe_list_should_print_received_recipe_and_user_answers_with_yes(self):
        """
            show recipe list should print received recipes
            and user answers with y -> both of the recipes are in liked list
        """
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.maxDiff = None
            with patch('builtins.input', return_value='yes'):
                self.__recipe_view.show_recipe_list()
                actual_stdout = fakeOutput.getvalue()
                self.assertTrue(all(match_str in actual_stdout for match_str in self.EXPECTED_RECIPE_OUTPUT_1))
                self.assertTrue(all(match_str in actual_stdout for match_str in self.EXPECTED_RECIPE_OUTPUT_2))

            actual_liked_recipe_list = self.__recipe_view.get_liked_recipe_list()
            self.assertEqual(len(actual_liked_recipe_list), 2)
            self.assertEqual(actual_liked_recipe_list, self.TEST_DATA)


    def test_show_recipe_list_should_print_received_recipe_and_user_answers_with_no(self):
        """
            show recipe list should print received recipes
            and user answers with no, liked list is empty
        """
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.maxDiff = None
            with patch('builtins.input', return_value='no'):
                self.__recipe_view.show_recipe_list()
                actual_stdout = fakeOutput.getvalue()
                self.assertTrue(all(match_str in actual_stdout for match_str in self.EXPECTED_RECIPE_OUTPUT_1))
                self.assertTrue(all(match_str in actual_stdout for match_str in self.EXPECTED_RECIPE_OUTPUT_2))

            actual_liked_recipe_list = self.__recipe_view.get_liked_recipe_list()
            self.assertEqual(len(actual_liked_recipe_list), 0)
            self.assertEqual(actual_liked_recipe_list, [])


if __name__ == '__main__':
    unittest.main()
