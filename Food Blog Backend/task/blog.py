#!/usr/bin/env python

import argparse


def cli_arguments():
    """ Handles command line arguments using argparse module. """
    parser = argparse.ArgumentParser(description='Accepts a single argument which is a database'
                                                 'name')
    parser.add_argument('db_name', type=str, help='Database name')
    return parser.parse_args()


db_name = cli_arguments().db_name
