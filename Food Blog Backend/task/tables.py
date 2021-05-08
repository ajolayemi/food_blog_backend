import sqlite3 as sq


class DatabaseCon:
    """ Creates database connection. """

    def __init__(self, database_name: str = None):
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

    def __init__(self, database_name: str, meal_names: list):
        super().__init__(database_name)
        self.meal_names = meal_names

        self.table_creator()

    def populate_meal_table(self):
        """ Populates meals table. """
        for meal in self.meal_names:
            if meal:
                query = f"INSERT INTO meals(meal_name) VALUES('{meal}')"
                self.cursor.execute(query)
        self.connection.commit()

    def table_creator(self):
        """ Creates meals table. """
        query = f'CREATE TABLE IF NOT EXISTS  {MealsTable.table_name} (' \
                f'meals_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                f'meal_name VARCHAR(20) NOT NULL UNIQUE )'
        self.cursor.execute(query)
        self.connection.commit()


class IngredientTable(DatabaseCon):
    table_name = 'ingredients'

    def __init__(self, ingredient_name: str):
        super().__init__()
        self.ingredient = ingredient_name

        self.table_creator()

    def populate_ingredient_table(self):
        query = f"INSERT INTO ingredients(ingredient_name) VALUES('{self.ingredient}')"
        self.cursor.execute(query)
        self.connection.commit()

    def table_creator(self):
        """ Creates ingredients table """
        query = f'CREATE TABLE IF NOT EXISTS {IngredientTable.table_name} (' \
                f'ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT ,' \
                f'ingredient_name VARCHAR(20) NOT NULL UNIQUE )'
        self.cursor.execute(query)
        self.connection.commit()


class MeasureTable(DatabaseCon):
    table_name = 'measures'

    def __init__(self, name: str):
        super().__init__()
        self.measure_name = name

        self.table_creator()

    def populate_measure_table(self):
        query = f"INSERT INTO measures(measure_name) VALUES ('{self.measure_name}')"
        self.cursor.execute(query)
        self.connection.commit()

    def table_creator(self):
        query = f'CREATE TABLE IF NOT EXISTS {MeasureTable.table_name} (' \
                f'measure_id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                f'measure_name VARCHAR(20) NOT NULL UNIQUE)'
        self.cursor.execute(query)
        self.connection.commit()
