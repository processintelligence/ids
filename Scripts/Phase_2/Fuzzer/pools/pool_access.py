import json
import random
from pathlib import Path

POOL_DIR = Path(__file__).parent

def get_random_value(json_filename):
    path = POOL_DIR / json_filename
    with open(path, "r") as f:
        data = json.load(f)

    return random.choice(list(data.values()))

def get_random_key_value(json_filename):
    path = POOL_DIR / json_filename
    with open(path, "r") as f:
        data = json.load(f)

    key_value_pair = random.choice(list(data.values()))

    key, value = key_value_pair.split(":")

    return key, value

