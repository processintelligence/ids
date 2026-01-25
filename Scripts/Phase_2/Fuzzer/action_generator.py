import random
from enum import Enum

# Generate a list of actions based on our grammar

# TERMINAL SYMBOLS

class MainLogon(str, Enum):
    INTERACTIVE = "Interactive_Logon"


class SubLogon(str, Enum):
    NETWORK = "Network_Logon"


class ObjectOp(str, Enum):
    CREATE = "Create_Object"
    DELETE = "Delete_Object"
    MODIFY = "Modify_Object"


class ProcessOp(str, Enum):
    GENERIC = "Start_Process"
    CMD = "Start_CMD_Process"


class Logoff(str, Enum):
    INTERACTIVE = "Interactive_Logoff"
    NETWORK = "Network_Logoff"


# PRODUCTION RULES

def generate_SESSION():
    events = []
    events.extend(generate_MAIN_LOGON())
    return events


def generate_MAIN_LOGON():
    events = []
    
    events.append(MainLogon.INTERACTIVE.value)
    events.extend(generate_ACTIONS())
    events.append(Logoff.INTERACTIVE.value)

    return events


def generate_ACTIONS():
    events = []
    num_actions = random.randint(0, 4)

    for _ in range(num_actions):
        events.extend(generate_ACTION())

    return events


def generate_ACTION():
    r = random.random()

    # 50%
    if r < 0.5:
        return generate_SUBLOGON()
    # 30%
    elif r < 0.8:
        return generate_OBJECT_OP()
    # 20%
    else:
        return generate_PROCESS_OP()


def generate_SUBLOGON():
    events = []

    events.append(SubLogon.NETWORK.value)
    events.append(Logoff.NETWORK.value)

    return events


def generate_OBJECT_OP():
    r = random.random()

    # 60%
    if r < 0.6:
        return [ObjectOp.MODIFY.value]
    # 30%
    elif r < 0.9:
        return [ObjectOp.CREATE.value] 
    # 10%
    else:
        return [ObjectOp.DELETE.value]


def generate_PROCESS_OP():
    # 70% 
    if random.random() < 0.7:
        return [ProcessOp.GENERIC.value]
    # 30%
    else:
        return [ProcessOp.CMD.value]


# TEST
if __name__ == "__main__":
    seq = generate_SESSION()
    for e in seq:
        print(e)
