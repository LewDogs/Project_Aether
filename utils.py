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

def str_to_obj(string):
    pairs = string.split(',')
    data = {k: int(v) for k, v in (pair.split(':') for pair in pairs)}

    return SimpleNamespace(**data)

def get_current_room_attr(world, element):
    world_attr = world.db_select(element, 'world', hero.current_location)
    try:
        return str_to_obj(world_attr)
    except:
        return exits

def get_item_attr(world, element, item):
    item_attr = world.db_select(element, 'world_items', item)
    try:
        return str_to_obj(item_attr)
    except:
        return item_attr

def items_str_to_obj(string, world):
    pairs = string.split(',')
    data = []
    for pair in pairs:
        vals = pair.split('x')
        name = get_item_attr(world, 'name', int(vals[1]))
        data.append({'num': int(vals[0]), 'item_id': int(vals[1]), 'name': name})
    return data
