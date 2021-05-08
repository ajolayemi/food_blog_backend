#!/usr/bin/env python

import argparse

from tables import (DatabaseCon, MealsTable, MeasureTable,
                    IngredientTable)

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


class PopulateTables:
    """ Populates all the 3 tables being used in this project. """

    @staticmethod
    def populate_meals_table():
        meal_data = list(data.get("meals"))
        meal_table_class = MealsTable(database_name=db_name, meal_names=meal_data)
        meal_table_class.populate_meal_table()


if __name__ == '__main__':
    PopulateTables.populate_meals_table()