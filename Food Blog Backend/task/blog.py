#!/usr/bin/env python

import argparse
import sys

from tables import (MealsTable, MeasureTable,
                    IngredientTable, RecipeTable,
                    ServeTable, QuantityTable)

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


def cli_arguments():
    """ Handles command line arguments using argparse module. """
    parser = argparse.ArgumentParser(description='Accepts a single argument which is a database'
                                                 'name')
    parser.add_argument('db_name', type=str, help='Database name')
    parser.add_argument('--ingredients', help='Pass in a list of ingredient names separated by comma.')
    parser.add_argument('--meals', help='Pass in a list of meal names separated by comma.')
    return parser.parse_args()


db_name = cli_arguments().db_name
if cli_arguments().ingredients:
    user_ingredients = tuple(cli_arguments().ingredients.split(','))
else:
    user_ingredients = None

if cli_arguments().meals:
    meals = tuple(cli_arguments().meals.split(','))
else:
    meals = None

if db_name:
    pass
else:
    print('No database name was passed!')
    sys.exit()


class BlogBackend:
    """ The food blog backend that communicates with the
    3 database tables being used in this project. """

    @staticmethod
    def recommend_recipe():
        ingredient_class = IngredientTable(database_name=db_name)
        ingredient_class.table_creator()

        meal_class = MealsTable(database_name=db_name)
        meal_class.table_creator()

        serve_class = ServeTable(database_name=db_name)
        serve_class.create_table()

        quantity_class = QuantityTable(database_name=db_name)
        quantity_class.create_table()

        recipe_class = RecipeTable(database_name=db_name)
        recipe_class.create_table()

        ingredients_ids = ingredient_class.get_ingredient_ids(ingredient_names=user_ingredients)
        matching_recipes = quantity_class.get_recipe_ids(ingredient_ids=ingredients_ids)
        meal_ids = meal_class.get_meal_ids(meal_names=meals)
        final_result = serve_class.recommend_recipe(recipe_ids=matching_recipes, meal_ids=meal_ids)
        print(f'Recipes selected for you: {recipe_class.get_recipe_names(recipe_ids=final_result)}')

    @staticmethod
    def populate_recipe_table():
        recipe_class = RecipeTable(database_name=db_name)
        recipe_class.create_table()

        serve_class = ServeTable(database_name=db_name)
        serve_class.create_table()

        ingredient_class = IngredientTable(database_name=db_name)
        ingredient_class.table_creator()

        measure_class = MeasureTable(database_name=db_name)
        measure_class.table_creator()

        quantity_table_class = QuantityTable(database_name=db_name)
        quantity_table_class.create_table()
        print('Pass the empty recipe name to exit')
        while True:
            recipe_name = input('Recipe name: ')
            if not recipe_name:
                break
            else:
                recipe_description = input('Recipe description: ')
                meal_cls = MealsTable(database_name=db_name)
                recipe_id = recipe_class.populate_table(recipe_name=recipe_name,
                                                        recipe_description=recipe_description)
                print(meal_cls)
                dish_time = input('When the dish can be served: ').split(' ')
                serve_class.populate_table(meals=dish_time,
                                           recipe_id=recipe_id)
                while True:
                    ingredients_info = input('Input quantity of ingredient <press enter to stop>: ').split(' ')
                    if not ingredients_info[0]:
                        break
                    elif len(ingredients_info) == 2:
                        quantity, ingredient = ingredients_info[0], ingredients_info[1]
                        measure = ''
                    else:
                        quantity, measure, ingredient = ingredients_info[0], ingredients_info[1], ingredients_info[2]
                    check_measure = measure_class.get_measure_names(measure)
                    ingredient_check = ingredient_class.get_ingredients(ingredient)
                    if len(check_measure) == 0 or len(check_measure) > 1:
                        print(f'The measure value -- {measure} -- entered is invalid!')
                    elif len(ingredient_check) == 0 or len(ingredient_check) > 1:
                        print(f'The ingredient -- {ingredient} -- is invalid!')
                    else:
                        quantity_table_class.populate_table(ingredient_id=ingredient_check[0][1],
                                                            measure_id=check_measure[0][1],
                                                            quantity=quantity,
                                                            recipe_id=recipe_id)

        recipe_class.connection.close()
        serve_class.connection.close()
        quantity_table_class.connection.close()
        measure_class.connection.close()
        ingredient_class.connection.close()

    @staticmethod
    def populate_measures_table():
        measures = list(data.get("measures"))
        measure_class = MeasureTable(database_name=db_name)
        measure_class.table_creator()
        measure_class.populate_table(measure_names=measures)
        measure_class.connection.close()

    @staticmethod
    def populate_ingredient_table():
        ingredients = list(data.get("ingredients"))
        ingredients_class = IngredientTable(database_name=db_name)
        ingredients_class.table_creator()
        ingredients_class.populate_table(ingredients)
        ingredients_class.connection.close()

    @staticmethod
    def populate_meals_table():
        meal_data = list(data.get("meals"))
        meal_table_class = MealsTable(database_name=db_name)
        meal_table_class.table_creator()
        meal_table_class.populate_table(meal_names=meal_data)
        meal_table_class.connection.close()


def main():
    backend = BlogBackend()
    if not user_ingredients and not meals:
        backend.populate_meals_table()
        backend.populate_ingredient_table()
        backend.populate_measures_table()
        backend.populate_recipe_table()
    else:
        backend.recommend_recipe()


if __name__ == '__main__':
    main()
