import json
import random
from pathlib import Path

POOL_DIR = Path(__file__).parent

def _load_json(filename):
    path = POOL_DIR / filename
    with open(path, "r") as f:
        return json.load(f)


def getrandomfile(): # TODO: Should there be delete files and create files?
    files = _load_json("files.json") # TODO: Are these files safe to modify/delete?
    return random.choice(list(files.values()))


def getrandomprocess():
    processes = _load_json("processes.json")
    return random.choice(list(processes.values()))


def getrandomuserpass(): # TODO: Should the return be (user, password)?
    users = _load_json("users.json") # TODO: We should add these users on the VM
    return random.choice(list(users.values())) # TODO: Should the json have user and password fields?

# TODO: get_random_registry_key