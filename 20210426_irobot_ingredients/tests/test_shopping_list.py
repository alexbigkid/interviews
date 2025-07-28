"""Unit tests for shopping_list.py"""

# Standard library imports
from io import StringIO
import unittest
from unittest.mock import patch

# Third party imports
from parameterized import parameterized

# Local application imports
from context import ShoppingList


class TestShoppingList(unittest.TestCase):
    RECIPE_LIST_TEST_DATA = [{"id":656323,"title":"Pita Pizzas with Sautéed Apples and Bacon","image":"https://spoonacular.com/recipeImages/656323-312x231.jpg","imageType":"jpg","usedIngredientCount":3,"missedIngredientCount":8,"missedIngredients":[{"id":18413,"amount":2,"unit":"","unitLong":"","unitShort":"","aisle":"Bakery/Bread","name":"pitas","original":"2 pitas","originalString":"2 pitas","originalName":"pitas","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/pita-bread.jpg"},{"id":10862,"amount":4,"unit":"slices","unitLong":"slices","unitShort":"slice","aisle":"Meat","name":"cooked bacon","original":"4 slices of bacon, cooked and crumbled","originalString":"4 slices of bacon, cooked and crumbled","originalName":"bacon, cooked and crumbled","metaInformation":["crumbled","cooked"],"meta":["crumbled","cooked"],"image":"https://spoonacular.com/cdn/ingredients_100x100/cooked-bacon.jpg"},{"id":10011282,"amount":0.5,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"red onion","original":"1/2 red onion, sliced","originalString":"1/2 red onion, sliced","originalName":"red onion, sliced","metaInformation":["red","sliced"],"meta":["red","sliced"],"image":"https://spoonacular.com/cdn/ingredients_100x100/red-onion.png"},{"id":1001009,"amount":0.75,"unit":"cup","unitLong":"cups","unitShort":"cup","aisle":"Cheese","name":"shredded cheddar cheese","original":"3/4 cup cheddar cheese, shredded","originalString":"3/4 cup cheddar cheese, shredded","originalName":"cheddar cheese, shredded","metaInformation":["shredded"],"meta":["shredded"],"image":"https://spoonacular.com/cdn/ingredients_100x100/shredded-cheddar.jpg"},{"id":2010,"amount":0.5,"unit":"teaspoon","unitLong":"teaspoons","unitShort":"tsp","aisle":"Spices and Seasonings","name":"cinnamon","original":"1/2 teaspoon cinnamon","originalString":"1/2 teaspoon cinnamon","originalName":"cinnamon","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/cinnamon.jpg"},{"id":1002011,"amount":1,"unit":"cloves","unitLong":"clove","unitShort":"cloves","aisle":"Spices and Seasonings","name":"cloves","original":"of cloves","originalString":"of cloves","originalName":"of","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/cloves.jpg"},{"id":1032009,"amount":0.75,"unit":"teaspoon","unitLong":"teaspoons","unitShort":"tsp","aisle":"Spices and Seasonings","name":"chili flakes","original":"3/4 teaspoon crushed chili pepper flakes","originalString":"3/4 teaspoon crushed chili pepper flakes","originalName":"crushed chili pepper flakes","metaInformation":["crushed"],"meta":["crushed"],"image":"https://spoonacular.com/cdn/ingredients_100x100/red-pepper-flakes.jpg"},{"id":1001,"amount":1,"unit":"tablespoon","unitLong":"tablespoon","unitShort":"Tbsp","aisle":"Milk, Eggs, Other Dairy","name":"butter","original":"1 tablespoon butter","originalString":"1 tablespoon butter","originalName":"butter","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/butter-sliced.jpg"}],"usedIngredients":[{"id":1089003,"amount":1,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"granny smith apple","original":"1 granny smith apple, cored and sliced","originalString":"1 granny smith apple, cored and sliced","originalName":"granny smith apple, cored and sliced","metaInformation":["cored","sliced"],"meta":["cored","sliced"],"image":"https://spoonacular.com/cdn/ingredients_100x100/grannysmith-apple.png"},{"id":11215,"amount":4,"unit":"cloves","unitLong":"cloves","unitShort":"cloves","aisle":"Produce","name":"garlic","original":"4 cloves of garlic, minced (divided)","originalString":"4 cloves of garlic, minced (divided)","originalName":"garlic, minced (divided)","metaInformation":["divided","minced","()"],"meta":["divided","minced","()"],"image":"https://spoonacular.com/cdn/ingredients_100x100/garlic.png"},{"id":2021,"amount":0.25,"unit":"teaspoon","unitLong":"teaspoons","unitShort":"tsp","aisle":"Spices and Seasonings","name":"ground ginger","original":"1/4 teaspoon ground ginger","originalString":"1/4 teaspoon ground ginger","originalName":"ground ginger","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}],"unusedIngredients":[{"id":11216,"amount":1,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce;Ethnic Foods;Spices and Seasonings","name":"ginger","original":"ginger","originalString":"ginger","originalName":"ginger","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}],"likes":1},{"id":647615,"title":"Huli-Huli Chicken","image":"https://spoonacular.com/recipeImages/647615-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":2,"missedIngredients":[{"id":1005006,"amount":6,"unit":"","unitLong":"","unitShort":"","aisle":"Meat","name":"chicken drumsticks and thighs","original":"6 CHICKEN DRUMSTICKS AND 4 THIGHS","originalString":"6 CHICKEN DRUMSTICKS AND 4 THIGHS","originalName":"CHICKEN DRUMSTICKS AND 4 THIGHS","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/chicken-parts.jpg"},{"id":9266,"amount":8,"unit":"ounces","unitLong":"ounces","unitShort":"oz","aisle":"Produce","name":"pineapple","original":"8 ounces crushed pineapple, undrained","originalString":"8 ounces crushed pineapple, undrained","originalName":"crushed pineapple, undrained","metaInformation":["crushed","undrained"],"meta":["crushed","undrained"],"image":"https://spoonacular.com/cdn/ingredients_100x100/pineapple.jpg"}],"usedIngredients":[{"id":11215,"amount":4,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"garlic cloves","original":"4 CLOVES GARLIC -SMASHED","originalString":"4 CLOVES GARLIC -SMASHED","originalName":"CLOVES GARLIC -SMASHED","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/garlic.png"},{"id":11216,"amount":4,"unit":"","unitLong":"","unitShort":"","aisle":"Produce;Ethnic Foods;Spices and Seasonings","name":"ginger root","original":"4 SLICES GINGER ROOT-SMASHED","originalString":"4 SLICES GINGER ROOT-SMASHED","originalName":"SLICES GINGER ROOT-SMASHED","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}],"unusedIngredients":[{"id":1089003,"amount":1,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"granny smith apple","original":"granny smith apple","originalString":"granny smith apple","originalName":"granny smith apple","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/grannysmith-apple.png"}],"likes":2}]
    RECIPE_LIST_TEST_DATA1 = [{"id":647615,"title":"Huli-Huli Chicken","image":"https://spoonacular.com/recipeImages/647615-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":2,"missedIngredients":[{"id":1005006,"amount":6,"unit":"","unitLong":"","unitShort":"","aisle":"Meat","name":"chicken drumsticks and thighs","original":"6 CHICKEN DRUMSTICKS AND 4 THIGHS","originalString":"6 CHICKEN DRUMSTICKS AND 4 THIGHS","originalName":"CHICKEN DRUMSTICKS AND 4 THIGHS","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/chicken-parts.jpg"},{"id":9266,"amount":8,"unit":"ounces","unitLong":"ounces","unitShort":"oz","aisle":"Produce","name":"pineapple","original":"8 ounces crushed pineapple, undrained","originalString":"8 ounces crushed pineapple, undrained","originalName":"crushed pineapple, undrained","metaInformation":["crushed","undrained"],"meta":["crushed","undrained"],"image":"https://spoonacular.com/cdn/ingredients_100x100/pineapple.jpg"}],"usedIngredients":[{"id":11215,"amount":4,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"garlic cloves","original":"4 CLOVES GARLIC -SMASHED","originalString":"4 CLOVES GARLIC -SMASHED","originalName":"CLOVES GARLIC -SMASHED","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/garlic.png"},{"id":11216,"amount":4,"unit":"","unitLong":"","unitShort":"","aisle":"Produce;Ethnic Foods;Spices and Seasonings","name":"ginger root","original":"4 SLICES GINGER ROOT-SMASHED","originalString":"4 SLICES GINGER ROOT-SMASHED","originalName":"SLICES GINGER ROOT-SMASHED","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"}],"unusedIngredients":[{"id":1089003,"amount":1,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"granny smith apple","original":"granny smith apple","originalString":"granny smith apple","originalName":"granny smith apple","metaInformation":[],"meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/grannysmith-apple.png"}],"likes":2}]
    PRICE_LIST_TEST_DATA1 = [{"ingredients":[{"name":"chicken drumsticks and thighs","image":"chicken-parts.jpg","price":254.32,"amount":{"metric":{"value":6,"unit":""},"us":{"value":6,"unit":""}}},{"name":"garlic cloves","image":"garlic.png","price":26.67,"amount":{"metric":{"value":4,"unit":""},"us":{"value":4,"unit":""}}},{"name":"ginger root","image":"ginger.png","price":15.49,"amount":{"metric":{"value":4,"unit":""},"us":{"value":4,"unit":""}}},{"name":"kosher salt","image":"salt.jpg","price":3.86,"amount":{"metric":{"value":2,"unit":"Tbsps"},"us":{"value":2,"unit":"Tbsps"}}},{"name":"pineapple","image":"pineapple.jpg","price":74.93,"amount":{"metric":{"value":226.796,"unit":"g"},"us":{"value":8,"unit":"ounces"}}}],"totalCost":375.27,"totalCostPerServing":62.54,"id":647615}]
    PRINT_PRETTY_TABLE_OUTPUT1 = '\
+-----------------------------------------------------------------------------------------------------------------+\n\
|                                                Huli-Huli Chicken                                                |\n\
| Missing ingredient list (well, most of them) | Aisle where to find missing ingredients in the store | Price ($) |\n\
| chicken drumsticks and thighs                | Meat                                                 |    254.32 |\n\
| pineapple                                    | Produce                                              |     74.93 |\n\
| Estimated cost for missing ingredients       |                                                      |    329.25 |\n\
| Estimated cost for all ingredients           |                                                      |    375.27 |\n\
\n\
\n\
\n\
+-----------------------------------------------------------------------+\n\
|                  Total cost / Recipes price breakdown                 |\n\
| Recipe name       | Missing ingredients costs | All ingredients costs |\n\
| Huli-Huli Chicken |                    329.25 |                375.27 |\n\
| Total sum         |                    329.25 |                375.27 |\n\
'

    PRINT_PRETTY_TABLE_OUTPUT2 = '\
+-----------------------------------------------------------------------------------------------------------------+\n\
|                                    Pita Pizzas with Sautéed Apples and Bacon                                    |\n\
| Missing ingredient list (well, most of them) | Aisle where to find missing ingredients in the store | Price ($) |\n\
| Price info for this recipe is not available  |                                                      |           |\n\
+-----------------------------------------------------------------------------------------------------------------+\n\
|                                                Huli-Huli Chicken                                                |\n\
| Missing ingredient list (well, most of them) | Aisle where to find missing ingredients in the store | Price ($) |\n\
| chicken drumsticks and thighs                | Meat                                                 |    254.32 |\n\
| pineapple                                    | Produce                                              |     74.93 |\n\
| Estimated cost for missing ingredients       |                                                      |    329.25 |\n\
| Estimated cost for all ingredients           |                                                      |    375.27 |\n\
\n\
\n\
\n\
+-----------------------------------------------------------------------------------------------+\n\
|                              Total cost / Recipes price breakdown                             |\n\
| Recipe name                               | Missing ingredients costs | All ingredients costs |\n\
| Pita Pizzas with Sautéed Apples and Bacon |                           |                       |\n\
| Huli-Huli Chicken                         |                    329.25 |                375.27 |\n\
| Total sum                                 |                    329.25 |                375.27 |\n\
'



    def setUp(self):
        self.__shopping_list = ShoppingList(self.RECIPE_LIST_TEST_DATA1, self.PRICE_LIST_TEST_DATA1)


    # -------------------------------------------------------------------------
    # Tests for condstructor
    # -------------------------------------------------------------------------
    @parameterized.expand([
        [[], [{'price_list': 'yes'}]],
        [[{'recipe_list': 'no'}], []],
        [[], []]
    ])
    def test_print_price_per_recipe_given_invalid_list_was_passed_in(self, recipe_list, price_list):
        """
            the constructor should throw an exception
            when invalid / empty recipe list is passed in
        """
        with self.assertRaises(Exception) as exception_message:
            self.__shopping_list = ShoppingList(recipe_list, price_list)
        self.assertEqual(str(exception_message.exception), self.__shopping_list.INVALID_NUMBER_OF_RECIPES_PASSED_IN)


    # -------------------------------------------------------------------------
    # Tests for print_price_per_recipe and print_final_result
    # -------------------------------------------------------------------------
    def test_print_price_per_recipe_produces_pretty_table_print(self):
        """
            print_price_per_recipe produces pretty table print for each recipe
            and the final cost table in pretty print
            given price list and recipe list are not empty
        """
        self.maxDiff = None
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.__shopping_list.print_price_per_recipe()
            self.__shopping_list.print_final_result()
            actual_stdout = fakeOutput.getvalue()
            self.assertEqual(actual_stdout, self.PRINT_PRETTY_TABLE_OUTPUT1)


    def test_print_price_per_recipe_produces_pretty_table_print_even_when_some_price_info_is_missing(self):
        """
            print_price_per_recipe produces pretty table print for each recipe
            and the final cost table in pretty print
            given price list and recipe list are not empty
            but price info for the recipe is missing
        """
        self.maxDiff = None
        self.__shopping_list = ShoppingList(self.RECIPE_LIST_TEST_DATA, self.PRICE_LIST_TEST_DATA1)
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            self.__shopping_list.print_price_per_recipe()
            self.__shopping_list.print_final_result()
            actual_stdout = fakeOutput.getvalue()
            self.assertEqual(actual_stdout, self.PRINT_PRETTY_TABLE_OUTPUT2)


    # -------------------------------------------------------------------------
    # Tests for print_final_result
    # -------------------------------------------------------------------------



if __name__ == '__main__':
    unittest.main()
