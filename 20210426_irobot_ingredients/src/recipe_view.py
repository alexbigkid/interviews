"""Shows user recipes. User is prompted to select recipes to his/her liking."""

# Standard library imports

# Third party imports
from colorama import Fore, Style

# Local application imports
from yes_no_generator import YesNoGenerator


class RecipeView():
    INVALID_NUMBER_OF_RECIPES_PASSED_IN = 'EXCEPTION: RecipeView invalid number of recipes passed in'
    TITLE_FOR_NUMBER_OF_RECIPES_FOUND = 'Number of recipes found matching provided ingredients'
    TITLE_FOR_RECIPE_NUMBER = 'Recipe number'
    TITLE_FOR_RECIPE_NAME = 'Recipe title'
    TITLE_FOR_PROVIDED_INGREDIENTS = 'Your ingredients'
    TITLE_FOR_MISSED_INGREDIENTS = 'Additional ingredients'
    RECIPE_TITLE_KEY = 'title'
    RECIPE_USED_INGREDIENTS_KEY = 'usedIngredients'
    RECIPE_MISSED_INGREDIENTS_KEY = 'missedIngredients'
    RECIPE_INGREDIENT_NAME_KEY = 'name'
    RECIPE_PROMPT_FOR_USER_LINE1 = 'Do you like the recipe? No maybe! Please answer with yes(y) or no(n)'
    RECIPE_PROMPT_FOR_USER_LINE2 = 'Anything else but "Yes" would be taken as "No"'
    RECIPE_PROMPT_FOR_USER_LINE3 = '> '


    def __init__(self, recipe_list):
        # protect module from invalid input in case it is taken out of this package
        # and used somewhere else
        if not len(recipe_list) > 0:
            raise Exception(self.INVALID_NUMBER_OF_RECIPES_PASSED_IN)
        self.__recipe_list = recipe_list
        self.__liked_recipe_list = []


    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def show_recipe_list(self):
        self.__print_number_of_recipes()
        for i, recipe in enumerate(self.__recipe_list):
            self.__print_recipe_number(str(i+1))
            self.__print_recipe(recipe)
            users_answer = self.__ask_user_for_selection()
            did_user_like_it = self.__did_user_like_the_recipe(users_answer)
            self.__print_users_answer_for_confirmation(did_user_like_it)
            if did_user_like_it:
                self.__liked_recipe_list.append(recipe)
            self.__print_separation_line('-')


    def get_liked_recipe_list(self):
        return self.__liked_recipe_list


    # -------------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------------
    def __print_number_of_recipes(self):
        print('\n\n')
        self.__print_title_line(self.TITLE_FOR_NUMBER_OF_RECIPES_FOUND, str(len(self.__recipe_list)))
        self.__print_separation_line('=')


    def __print_recipe_number(self, number_str):
        self.__print_title_line(self.TITLE_FOR_RECIPE_NUMBER, number_str)


    def __print_recipe(self, recipe):
        self.__print_title_line(self.TITLE_FOR_RECIPE_NAME, recipe[self.RECIPE_TITLE_KEY])
        self.__print_ingredients_line(self.TITLE_FOR_PROVIDED_INGREDIENTS, recipe[self.RECIPE_USED_INGREDIENTS_KEY])
        self.__print_ingredients_line(self.TITLE_FOR_MISSED_INGREDIENTS, recipe[self.RECIPE_MISSED_INGREDIENTS_KEY])


    def __print_title_line(self, title_name, value):
        print(': '.join([title_name, value]))


    def __print_separation_line(self, sign_to_print):
        print(sign_to_print * 80)


    def __print_ingredients_line(self, title_name, ingredient_list):
        list_length = len(ingredient_list)
        if list_length > 0:
            ingredients_str = ', '.join([ingredient[self.RECIPE_INGREDIENT_NAME_KEY] for ingredient in ingredient_list])
            self.__print_title_line(title_name, ingredients_str)


    def __ask_user_for_selection(self):
        print(Fore.YELLOW + f"{self.RECIPE_PROMPT_FOR_USER_LINE1}")
        print(self.RECIPE_PROMPT_FOR_USER_LINE2)
        return input(self.RECIPE_PROMPT_FOR_USER_LINE3)


    def __did_user_like_the_recipe(self, users_answer):
        yes_string = users_answer.lower()
        return yes_string == 'yes' or yes_string == 'y'

    def __print_users_answer_for_confirmation(self, did_user_like_it):
        yes_or_no = YesNoGenerator()
        if did_user_like_it:
            print('You answered with: ' + Fore.GREEN + f"{yes_or_no.generate_random_yes()}")
        else:
            print('You answered with: ' + Fore.RED + f"{yes_or_no.generate_random_no()}")
        print(f"{Style.RESET_ALL}")
