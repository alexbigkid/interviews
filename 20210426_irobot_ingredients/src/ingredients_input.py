"""Prompts user to enter ingredients, sanitizes user's input and validates it"""

class IngredientsInput():
    USER_PROMPT_FOR_INGREDIENTS = 'Please enter your favorite ingredients separated by comma:'
    INVALID_INPUT_EXCEPTION_MESSAGE = 'EXCEPTION: Ivalid input. Please use only letters and white spaces.'


    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def ask_for_ingredients(self):
        print(self.USER_PROMPT_FOR_INGREDIENTS)


    def read_input(self):
        ingredients = input('> ')
        ingredients = ingredients.split(',')
        ingredients = self.__sanitize_input(ingredients)
        if self.__is_input_valid(ingredients):
            return ingredients
        else:
            raise Exception(self.INVALID_INPUT_EXCEPTION_MESSAGE)


    # -------------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------------
    def __sanitize_input(self, ingredient_list):
        ingredients = [ingredient.strip(' ') for ingredient in ingredient_list]
        return list(filter(None, ingredients))


    def __is_input_valid(self, ingredient_list):
        return len(ingredient_list) != 0 and \
            all(ingredient.replace(' ','').isalpha() for ingredient in ingredient_list)
