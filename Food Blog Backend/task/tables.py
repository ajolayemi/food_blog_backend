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

    def populate_table(self):
        """ Populates meals table. """
        for meal in self.meal_names:
            if meal:
                query = f"INSERT INTO meals(meal_name) VALUES('{meal}')"
                self.cursor.execute(query)
        self.connection.commit()

    def table_creator(self):
        """ Creates meals table. """
        query = f'CREATE TABLE IF NOT EXISTS  {MealsTable.table_name} (' \
                f'meal_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                f'meal_name VARCHAR(20) NOT NULL UNIQUE )'
        self.cursor.execute(query)
        self.connection.commit()


class IngredientTable(DatabaseCon):
    table_name = 'ingredients'

    def __init__(self, database_name: str, ingredient_names: list):
        super().__init__(database_name)
        self.ingredients = ingredient_names

        self.table_creator()

    def populate_table(self):
        for ingredient in self.ingredients:
            if ingredient:
                query = f"INSERT INTO ingredients(ingredient_name) VALUES('{ingredient}')"
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

    def __init__(self, database_name: str, measure_names: list):
        super().__init__(database_name)
        self.measure_names = measure_names

        self.table_creator()

    def populate_table(self):
        for measure in self.measure_names:
            query = f"INSERT INTO measures(measure_name) VALUES ('{measure}')"
            self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()

    def table_creator(self):
        query = f'CREATE TABLE IF NOT EXISTS {MeasureTable.table_name} (' \
                f'measure_id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                f'measure_name VARCHAR(20) UNIQUE)'
        self.cursor.execute(query)
        self.connection.commit()


class RecipeTable(DatabaseCon):
    table_name = 'recipes'

    def __init__(self, database_name: str = None, recipe_name: str = None,
                 recipe_description: str = None):
        super().__init__(database_name)
        self.recipe = recipe_name
        self.description = recipe_description

    def populate_table(self):
        query = f"INSERT INTO recipes(recipe_name, recipe_description) VALUES(" \
                f"'{self.recipe}', '{self.description}')"
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()

    def create_table(self):
        query = f'CREATE TABLE IF NOT EXISTS {RecipeTable.table_name} (' \
                f'recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                f'recipe_name VARCHAR(40) NOT NULL,' \
                f'recipe_description VARCHAR(100))'
        self.cursor.execute(query)
        self.connection.commit()
