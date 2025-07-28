"""Main program for displaying ingredients list for shopping with the recipes liked"""

# Standard library imports
import sys

# Third party imports
from colorama import Fore, Style

# Local application imports
from ingredients_input import IngredientsInput
from search_recipes_by_ingredients import SearchRecipesByIngredients
from recipe_view import RecipeView
from shopping_list import ShoppingList
from recipe_price_breakdown import RecipePriceBreakdown

def get_ingredients():
    ingredients_input = IngredientsInput()
    ingredients_input.ask_for_ingredients()
    return ingredients_input.read_input()


def get_recipes(ingredients):
    search_recipes = SearchRecipesByIngredients()
    return search_recipes.get_recipes(ingredients)


def get_liked_recipes(recipes):
    recipe_selection = RecipeView(recipes)
    recipe_selection.show_recipe_list()
    return recipe_selection.get_liked_recipe_list()


def get_price_info(liked_recipe_list):
    recipe_price = RecipePriceBreakdown(liked_recipe_list)
    return recipe_price.get_price_breakdown()


def show_shopping_list(liked_recipe_list, price_info_list):
    shopping_list = ShoppingList(liked_recipe_list, price_info_list)
    shopping_list.print_price_per_recipe()
    shopping_list.print_final_result()


def main():
    exit_code = 0
    try:
        ingredient_list = get_ingredients()
        # ingredient_list = ['garlic', 'ginger', 'granny smith apple']
        recipe_list = get_recipes(ingredient_list)
        liked_recipe_list = get_liked_recipes(recipe_list)
        price_info_list = get_price_info(liked_recipe_list)
        show_shopping_list(liked_recipe_list, price_info_list)
    except Exception as exception:
        print(Fore.RED + f"ERROR: executing getting recipes with your favorite ingredients")
        print(f"{exception}{Style.RESET_ALL}")
        exit_code = 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
