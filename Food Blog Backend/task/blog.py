#!/usr/bin/env python

import sqlite3 as sq
import argparse


def cli_arguments():
    """ Handles command line arguments using argparse module. """
    parser = argparse.ArgumentParser(description='Accepts a single argument which is a database'
                                                 'name')
    parser.add_argument('db_name', type=str, help='Database name')
    return parser.parse_args()


db_name = cli_arguments().db_name


class DatabaseCon:
    """ Creates database connection. """

    def __init__(self, database_name: str = db_name):
        self.db = database_name
        self.cursor = None
        self.connection = None

        self.create_con()

    def create_con(self):
        """ Creates database connection. """
        self.connection = sq.connect(self.db)
        self.cursor = self.connection.cursor()

    def __str__(self):
        """ A string representation of this class """
        return f'A database named "{self.db}" has been created. '

    def __repr__(self):
        return f'Database [(name, {self.db}), (cursor, {self.cursor}), ' \
               f'(connection, {self.connection}]'


class MealsTable(DatabaseCon):
    table_name = 'meals'

    def __init__(self, meal_id: int, meal_name: str):
        super().__init__()
        self.meal_id = meal_id
        self.meal_name = meal_name

        self.table_creator()

    def populate_table(self):
        """ Populates meals table. """
        query = f'INSERT INTO meals (meal_id, meal_name) VALUES (' \
                f'{self.meal_id}, {self.meal_name})'
        self.cursor.execute(query)
        self.connection.commit()

    def table_creator(self):
        """ Creates meals table. """
        query = f'CREATE TABLE IF NOT EXISTS  {MealsTable.table_name} (' \
                f'meals_id INT PRIMARY KEY,' \
                f'meal_name VARCHAR(20) NOT NULL UNIQUE )'
        self.cursor.execute(query)
        self.connection.commit()


class IngredientTable(DatabaseCon):
    table_name = 'ingredients'

    def __init__(self, ingredient_id: int, ingredient_name: str):
        super().__init__()
        self.ingredient_id = ingredient_id
        self.ingredient = ingredient_name

        self.table_creator()

    def populate_ingredient_table(self):
        query = f'INSERT INTO ingredients (ingredient_id, ingredient_name) VALUES (' \
                f'{self.ingredient_id}, {self.ingredient})'
        self.cursor.execute(query)
        self.connection.commit()

    def table_creator(self):
        """ Creates ingredients table """
        query = f'CREATE TABLE IF NOT EXISTS {IngredientTable.table_name} (' \
                f'ingredient_id INT PRIMARY KEY,' \
                f'ingredient_name VARCHAR(20) NOT NULL UNIQUE )'
        self.cursor.execute(query)
        self.connection.commit()


if __name__ == '__main__':
    a = IngredientTable(1, 's')



