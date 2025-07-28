"""Gets the price breakdown and shows final result."""

# Standard library imports

# Third party imports
from colorama import Fore, Style
import json
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY

# Local application imports


class ShoppingList():
    INVALID_NUMBER_OF_RECIPES_PASSED_IN = 'No recipe selected to show in the shopping list'
    RECIPE_ID_KEY = 'id'
    RECIPE_TITTLE_KEY = 'title'
    INGREDIENT_NAME_KEY = 'name'
    INGREDIENT_PRICE_KEY = 'price'
    INGREDIENT_AISLE_NAME_KEY = 'aisle'
    MISSING_INGREDIENTS_KEY = 'missedIngredients'
    PRICE_LIST_INGREDIENT_KEY = 'ingredients'
    PRICE_LIST_TOTAL_COST_KEY = 'totalCost'
    PRETTY_TABLE_INGREDIENT = 'Missing ingredient list (well, most of them)'
    PRETTY_TABLE_AISLE = 'Aisle where to find missing ingredients in the store'
    PRETTY_TABLE_PRICE = 'Price ($)'
    ESTIMATED_COST_FOR_MISSING_INGREDIENTS_TEXT = 'Estimated cost for missing ingredients'
    ESTIMATED_COST_FOR_ALL_INGREDIENTS_TEXT = 'Estimated cost for all ingredients'
    ESTIMATED_COST_NOT_AVAILABLE_TEXT = 'Price info for this recipe is not available'
    TOTAL_COST_MISSING_INGREDIENTS = 'missedIngredientsCost'
    TOTAL_COST_ALL_INGREDIENTS = 'allIngredientsCost'
    NO_PRICE_INFO_AVAiLABLE_TEXT = 'Unfortunatelly, no price info available'
    FINAL_RESULT_TABLE_HEADER_RECIPE_NAME = 'Recipe name'
    FINAL_RESULT_TABLE_HEADER_MISSING_INGREDIETS = 'Missing ingredients costs'
    FINAL_RESULT_TABLE_HEADER_ALL_INGREDIETS = 'All ingredients costs'
    FINAL_RESULT_SUM = 'Total sum'
    FINAL_RESULT_TABLE_HEADER = 'Total cost / Recipes price breakdown'


    def __init__(self, liked_recipe_list, price_info_list):
        # protect module from invalid input in case it is taken out of this package
        # and used somewhere else
        if not len(liked_recipe_list) > 0:
            raise Exception(self.INVALID_NUMBER_OF_RECIPES_PASSED_IN)
        if not len(price_info_list) > 0:
            raise Exception(self.INVALID_NUMBER_OF_RECIPES_PASSED_IN)
        self.__liked_recipe_list = liked_recipe_list
        self.__price_list = price_info_list
        self.__total_price_for_all_recipes = []


    # -------------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------------
    def print_price_per_recipe(self):
        if not len(self.__price_list) > 0:
            print(self.NO_PRICE_INFO_AVAiLABLE_TEXT)
            return
        self.__print_price_per_recipe()


    def print_final_result(self):
        if not len(self.__total_price_for_all_recipes) > 0:
            print(self.NO_PRICE_INFO_AVAiLABLE_TEXT)
            return
        self.__print_recipe_total_costs()


    # -------------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------------
    def __print_price_per_recipe(self):
        i = 0
        for liked_recipe in self.__liked_recipe_list:
            if liked_recipe[self.RECIPE_ID_KEY] == self.__price_list[i][self.RECIPE_ID_KEY]:
                self.__print_info_for_all_missing_ingredients_in_recipe_and_save_total_costs(liked_recipe, self.__price_list[i])
                i += 1
            else:
                self.__print_price_info_not_avaibale(liked_recipe)


    # todo: this method needs refactoring since it is doing more then 1 thing
    def __print_info_for_all_missing_ingredients_in_recipe_and_save_total_costs(self, recipe, price_breakdown):
        missed_ingredient_list = recipe[self.MISSING_INGREDIENTS_KEY]
        ingredient_price_list = price_breakdown[self.PRICE_LIST_INGREDIENT_KEY]
        total_missed_ingredients_price = 0.0
        header_list = [self.PRETTY_TABLE_INGREDIENT, self.PRETTY_TABLE_AISLE, self.PRETTY_TABLE_PRICE]
        alignment_list = ['l', 'l', 'r']
        pretty_table = self.__create_pretty_table_recipe_header(header_list, alignment_list)

        for missed_ingredient in missed_ingredient_list:
            for ingredient_price in ingredient_price_list:
                if missed_ingredient[self.INGREDIENT_NAME_KEY] == ingredient_price[self.INGREDIENT_NAME_KEY]:
                    pretty_table.add_row([
                        missed_ingredient[self.INGREDIENT_NAME_KEY],
                        missed_ingredient[self.INGREDIENT_AISLE_NAME_KEY],
                        str(ingredient_price[self.INGREDIENT_PRICE_KEY])
                    ])
                    total_missed_ingredients_price += ingredient_price[self.INGREDIENT_PRICE_KEY]
        # round needed because computer sometime have trouble to calculate floating points
        total_missed_ingredients_price = round(total_missed_ingredients_price,2)
        pretty_table.add_row([self.ESTIMATED_COST_FOR_MISSING_INGREDIENTS_TEXT, '', str(total_missed_ingredients_price)])
        pretty_table.add_row([self.ESTIMATED_COST_FOR_ALL_INGREDIENTS_TEXT, '', str(price_breakdown[self.PRICE_LIST_TOTAL_COST_KEY])])
        print(pretty_table.get_string(title=recipe[self.RECIPE_TITTLE_KEY]))

        self.__save_total_price_info_to_be_used_later(recipe[self.RECIPE_ID_KEY], total_missed_ingredients_price, price_breakdown[self.PRICE_LIST_TOTAL_COST_KEY])


    def __save_total_price_info_to_be_used_later(self, recipe_id, missed_ingredients_costs, all_ingredients_costs):
        self.__total_price_for_all_recipes.append({
            self.RECIPE_ID_KEY: recipe_id,
            self.TOTAL_COST_MISSING_INGREDIENTS: missed_ingredients_costs,
            self.TOTAL_COST_ALL_INGREDIENTS: all_ingredients_costs
        })


    def __print_price_info_not_avaibale(self, recipe):
        header_list = [self.PRETTY_TABLE_INGREDIENT, self.PRETTY_TABLE_AISLE, self.PRETTY_TABLE_PRICE]
        alignment_list = ['l', 'l', 'r']
        pretty_table = self.__create_pretty_table_recipe_header(header_list, alignment_list)
        pretty_table.add_row([self.ESTIMATED_COST_NOT_AVAILABLE_TEXT, '', ''])
        print(pretty_table.get_string(title=recipe[self.RECIPE_TITTLE_KEY]))


    def __create_pretty_table_recipe_header(self, field_name_list, field_alignment_list):
        pretty_table = PrettyTable()
        pretty_table.set_style(MSWORD_FRIENDLY)
        pretty_table.field_names = field_name_list
        pretty_table.align[field_name_list[0]] = field_alignment_list[0]
        pretty_table.align[field_name_list[1]] = field_alignment_list[1]
        pretty_table.align[field_name_list[2]] = field_alignment_list[2]
        return pretty_table


    def __print_recipe_total_costs(self):
        pretty_table = self.__generate_pretty_table_for_total_cost()
        i = 0
        total_missing_ingredients_cost = 0.0
        total_all_ingredients_cost = 0.0
        for liked_recipe in self.__liked_recipe_list:
            if liked_recipe[self.RECIPE_ID_KEY] == self.__total_price_for_all_recipes[i][self.RECIPE_ID_KEY]:
                total_missing_ingredients_cost += self.__total_price_for_all_recipes[i][self.TOTAL_COST_MISSING_INGREDIENTS]
                total_all_ingredients_cost += self.__total_price_for_all_recipes[i][self.TOTAL_COST_ALL_INGREDIENTS]
                pretty_table.add_row([
                    liked_recipe[self.RECIPE_TITTLE_KEY],
                    self.__total_price_for_all_recipes[i][self.TOTAL_COST_MISSING_INGREDIENTS],
                    self.__total_price_for_all_recipes[i][self.TOTAL_COST_ALL_INGREDIENTS]
                ])
                i += 1
            else:
                pretty_table.add_row([liked_recipe[self.RECIPE_TITTLE_KEY], '', ''])
        total_missing_ingredients_cost = round(total_missing_ingredients_cost, 2)
        total_all_ingredients_cost = round(total_all_ingredients_cost, 2)
        pretty_table.add_row([self.FINAL_RESULT_SUM, str(total_missing_ingredients_cost), str(total_all_ingredients_cost)])
        print('\n\n')
        print(pretty_table.get_string(title=self.FINAL_RESULT_TABLE_HEADER))


    def __generate_pretty_table_for_total_cost(self):
        header_list = [
            self.FINAL_RESULT_TABLE_HEADER_RECIPE_NAME,
            self.FINAL_RESULT_TABLE_HEADER_MISSING_INGREDIETS,
            self.FINAL_RESULT_TABLE_HEADER_ALL_INGREDIETS
        ]
        alignment_list = ['l', 'r', 'r']
        return self.__create_pretty_table_recipe_header(header_list, alignment_list)
