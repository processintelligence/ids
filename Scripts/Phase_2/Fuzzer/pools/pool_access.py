import json
import random
from pathlib import Path

POOL_DIR = Path(__file__).parent

def _load_json(filename):
    path = POOL_DIR / filename
    with open(path, "r") as f:
        return json.load(f)


def getrandomfile():
    files = _load_json("files.json")
    return random.choice(list(files.values()))


def getrandomprocess():
    processes = _load_json("processes.json")
    return random.choice(list(processes.values()))


def getrandomuserpass():
    users = _load_json("users.json")
    return random.choice(list(users.values()))
