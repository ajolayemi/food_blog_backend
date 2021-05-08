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

    def __init__(self, database_name: str, meal_names: list = None):
        super().__init__(database_name)
        self.meal_names = meal_names

        self.table_creator()

    def __str__(self):
        """ A string representation of this table which
        returns all meals available in the table"""
        query = f"SELECT meal_id, meal_name FROM meals"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        output = ''
        for meal in results:
            output += f'{meal[0]}) {meal[1]}  '
        return output

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

    def __init__(self, database_name: str, measure_names: list = None):
        super().__init__(database_name)
        self.measure_names = measure_names

        self.table_creator()

    def get_measure_names(self, letter: str):
        """ Get's all measure names starting with letter. """
        query = f"SELECT measure_name FROM measures WHERE measure_name >= '{letter}'"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        matching_measures = [measure[0] for measure in results if measure[0].startswith(letter)]
        return matching_measures

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
        return self.cursor.lastrowid

    def create_table(self):
        query = f'CREATE TABLE IF NOT EXISTS {RecipeTable.table_name} (' \
                f'recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                f'recipe_name VARCHAR(40) NOT NULL,' \
                f'recipe_description VARCHAR(100))'
        self.cursor.execute(query)
        self.connection.commit()


class ServeTable(DatabaseCon):
    table_name = 'serve'

    def __init__(self, database_name: str, meal_ids: list = None,
                 recipe_id: int = None):
        super(ServeTable, self).__init__(database_name)
        self.meals = meal_ids
        self.recipe = recipe_id

    def populate_table(self):
        for meal_id in self.meals:
            if meal_id:
                query = f"INSERT INTO serve(recipe_id, meal_id) VALUES ({self.recipe}, " \
                        f"{meal_id})"
                self.cursor.execute(query)
        self.connection.commit()
        self.connection.close()

    def create_table(self):
        query = f'CREATE TABLE IF NOT EXISTS {ServeTable.table_name} (' \
                f'serve_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                f'recipe_id INTEGER NOT NULL,' \
                f'meal_id INTEGER NOT NULL,' \
                f'FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),' \
                f'FOREIGN KEY(meal_id) REFERENCES meals(meal_id))'
        self.cursor.execute(query)
        self.connection.commit()


class QuantityTable(DatabaseCon):
    table_name = 'quantity'

    def __init__(self, database_name: str):
        super().__init__(database_name)

    def create_table(self):
        query = f'CREATE TABLE IF NOT EXISTS {QuantityTable.table_name} (' \
                f'quantity_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
                f'measure_id INTEGER NOT NULL,' \
                f'ingredient_id INTEGER NOT NULL,' \
                f'quantity INTEGER NOT NULL,' \
                f'recipe_id INTEGER NOT NULL,' \
                f'FOREIGN KEY(measure_id) REFERENCES measures(measure_id),' \
                f'FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),' \
                f'FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id))'
        self.cursor.execute(query)
        self.connection.commit()
