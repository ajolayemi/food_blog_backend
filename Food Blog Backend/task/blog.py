#!/usr/bin/env python

import argparse
import sys

from tables import (MealsTable, MeasureTable,
                    IngredientTable, RecipeTable,
                    ServeTable)

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}


def cli_arguments():
    """ Handles command line arguments using argparse module. """
    parser = argparse.ArgumentParser(description='Accepts a single argument which is a database'
                                                 'name')
    parser.add_argument('db_name', type=str, help='Database name')
    return parser.parse_args()


db_name = cli_arguments().db_name
if db_name:
    pass
else:
    print('No database name was passed!')
    sys.exit()


class PopulateTables:
    """ Populates all the 3 tables being used in this project. """

    @staticmethod
    def populate_recipe_table():
        RecipeTable(database_name=db_name).create_table()
        ServeTable(database_name=db_name).create_table()
        print('Pass the empty recipe name to exit')
        while True:
            recipe_name = input('Recipe name: ')
            if not recipe_name:
                break
            else:
                recipe_description = input('Recipe description: ')
                recipe_table_cls = RecipeTable(database_name=db_name,
                                               recipe_name=recipe_name,
                                               recipe_description=recipe_description)
                meal_cls = MealsTable(database_name=db_name)
                recipe_id = recipe_table_cls.populate_table()
                print(meal_cls)
                dish_time = input('When the dish can be served: ').split(' ')
                serve_table_cls = ServeTable(database_name=db_name,
                                             meal_ids=dish_time,
                                             recipe_id=recipe_id)
                serve_table_cls.populate_table()

    @staticmethod
    def populate_measures_table():
        measures = list(data.get("measures"))
        measure_class = MeasureTable(database_name=db_name,
                                     measure_names=measures)
        measure_class.populate_table()

    @staticmethod
    def populate_ingredient_table():
        ingredients = list(data.get("ingredients"))
        ingredients_class = IngredientTable(database_name=db_name, ingredient_names=ingredients)
        ingredients_class.populate_table()

    @staticmethod
    def populate_meals_table():
        meal_data = list(data.get("meals"))
        meal_table_class = MealsTable(database_name=db_name, meal_names=meal_data)
        meal_table_class.populate_table()


def main():
    data_writer_cls = PopulateTables()
    data_writer_cls.populate_meals_table()
    data_writer_cls.populate_ingredient_table()
    data_writer_cls.populate_measures_table()
    data_writer_cls.populate_recipe_table()


if __name__ == '__main__':
    main()
