import os
import csv
import sqlite3
from player import Player
from types import SimpleNamespace

# Base directory path for finding csv files in this project
base_dir = os.path.dirname(os.path.abspath(__file__))

hero = Player()

def next_prompt(prompt):
    print(prompt)
    print("--------")

def load_map_file(filename):
    file_data = []
    filepath = os.path.join(base_dir, 'World Files', filename)
    if not os.path.exists(filepath):
        print(f"Error: Could not find {filepath}!")
        return file_data
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            file_data.append(row)
    return file_data

def get_exits(world):
    exits = str_to_obj(world.db_select('exits', 'world', hero.current_location))
    return exits

def str_to_obj(string):
    pairs = string.split(',')
    data = {k: int(v) for k, v in (pair.split(':') for pair in pairs)}

    return SimpleNamespace(**data)