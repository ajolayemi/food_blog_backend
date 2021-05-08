#!/usr/bin/env python

import sqlite3 as sq
import argparse


def cli_arguments():
    """ Handles command line arguments using argparse module. """
    parser = argparse.ArgumentParser(description='Accepts a single argument which is a database'
                                                 'name')
    parser.add_argument('dd_name', type=str, help='Database name')
    return parser.parse_args()


class DatabaseCon:
    """ Creates database connection. """

    def __init__(self, database_name: str):
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


if __name__ == '__main__':
    a = DatabaseCon('test')
    print(a.__repr__())