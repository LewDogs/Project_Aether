from types import SimpleNamespace
import utils
import sqlite3
import os
import csv
from player import Player

# Base directory path for finding csv files in this project
base_dir = os.path.dirname(os.path.abspath(__file__))

hero = Player()

class World:
    _instance = None  # This stores the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the instance only if it doesn't exist
            cls._instance = super(World, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        self.connection = sqlite3.connect(base_dir + '/aether.db')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.init_db()
    
    def begin(self):
        # Introduce the world
        utils.next_prompt(self.db_select('location_name', 'world', 1))
        utils.next_prompt(self.db_select('initial_description', 'world', 1))
        
        

    def load_file(self, table_name, filename):
        filepath = os.path.join(base_dir, 'World Files', filename)
        if not os.path.exists(filepath):
            print(f"Error: Could not find {filepath}!")
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Skip the header row (index, location_name, etc.)
            next(reader)

            for row in reader:
                # print("row", row)
                self.insert_dynamic(table_name, row)

    def insert_dynamic(self, table_name, row_dict):
        # Get column names from the row dictionary
        columns = ', '.join(row_dict.keys())

        # Create the placeholders, based on the number of items
        placeholders = ', '.join(['?'] * len(row_dict))

        # Construct the SQL command
        command = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"

        values = tuple(row_dict.values())

        self.cursor.execute(command, values)

    def init_db(self):
        # Create World table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS world (
            id int NOT NULL PRIMARY KEY,
            location_name TEXT,
            initial_description TEXT,
            description TEXT,
            exits BLOB,
            items BLOB,
            npcs TEXT,
            exit_items TEXT,
            enemies TEXT
        )
        ''')

        # Create Items table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS world_items (
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT,
            item_type TEXT,
            item_action TEXT,
            currency INTEGER,
            max_stack INTEGER,
            dmg_die TEXT,
            consumable INTEGER,
            special TEXT
        )
        ''')

        # Populate world and items tables
        self.load_file('world', 'world.csv')
        self.load_file('world_items', 'items.csv')
        
        # Commit the changes to save them
        self.connection.commit()

    def db_select(self, element, table, room):
        query = f"SELECT {element} FROM {table} WHERE id = ?"
        self.cursor.execute(query, (room,))
        val = self.cursor.fetchone()
        return val[0]
    
    def build_map(self, imported_map):
        self.world_map = imported_map
        return self.world_map

    def import_items(self, imported_items):
        self.world_items = imported_items
        return self.world_items

    def reveal_map(self):
        utils.next_prompt("Loading Map...")
        for row in self.world_map:
            vals = ""
            if (row != None):
                for item in row:
                    if item == '_':
                        vals += ' '
                    elif item == 'x' or item == '-' or item == '|':
                        vals = vals + item
                    elif int(item) in hero.visited:
                        vals = vals + str(item)
                    else:
                        vals = vals + '?'
            print(vals)
        print()
        print("--------")

    def on_quit(self):
        self.connection.close()

    def loc_name(self):
        return self.db_select('location_name', 'world', hero.current_location)
    
    def loc_desc(self):
        if hero.current_location in hero.visited:
            return self.db_select('description', 'world', hero.current_location)
        else:
            return self.db_select('initial_description', 'world', hero.current_location)

    def loc_exits(self):
        return utils.str_to_obj(self.db_select('exits', 'world', hero.current_location))

    def loc_items(self):
        return self.db_select('items', 'world', hero.current_location)
        
    def loc_npcs(self):
        return self.db_select('npcs', 'world', hero.current_location)
        
    def loc_exit_items(self):
        return self.db_select('exit_items', 'world', hero.current_location)
        
    def loc_enemies(self):
        return self.db_select('enemies', 'world', hero.current_location)
        