# Should rename this to something like action_generator.py
import random


# -------------------------------------------------------------
# TERMINAL SYMBOL GROUPS FROM YOUR GRAMMAR (exact names)
# -------------------------------------------------------------

SUCCESSFUL_MAIN_LOGONS = [
    "Interactive_Logon",
    "Network_Logon"
]

FAILED_LOGON = "Failed_Logon"

SUBLOGONS = [
    "Batch_Logon",
    "Service_Logon",
    "RunAs_Logon"
]

OBJECT_OPS = [
    "Create_Object",
    "Delete_Object",
    "Modify_Object"
]

REGISTRY_OPS = [
    "Create_Registry",
    "Delete_Registry",
    "Modify_Registry",
    "Modify_CommonStartup_Registry"
]

PROCESS_OPS_GENERIC = ["Start_Process"]
PROCESS_OPS_CMD = ["Start_CMD_Process"]

LOCK_UNLOCK_PAIR = ["Lock_Workstation", "Unlock_Workstation"]

LOGOFF = ["Logoff"]

SUBLOGOFF = ["Sub_Logoff"]


# -------------------------------------------------------------
# PRODUCTION RULES IMPLEMENTED AS PYTHON FUNCTIONS
# -------------------------------------------------------------

def generate_SESSION():
    events = []
    events.extend(generate_MAIN_LOGON())
    events.extend(generate_ACTIONS())
    events.extend(generate_MAIN_LOGOFF())
    return events


def generate_MAIN_LOGON():
    events = []

    # Generate 0–3 failed login attempts before success
    if random.random() < 0.25:
        failures = random.randint(1, 3)
        events.extend([FAILED_LOGON] * failures)

    # SUCCESSFUL_MAIN_LOGON
    events.append(random.choice(SUCCESSFUL_MAIN_LOGONS))

    return events


def generate_MAIN_LOGOFF():
    return [random.choice(LOGOFF)]


def generate_ACTIONS(depth=0, max_depth=2):
    events = []

    num_actions = random.randint(0, 4)

    for _ in range(num_actions):
        events.extend(generate_ACTION(depth=depth, max_depth=max_depth))

    return events


def generate_ACTION(depth=0, max_depth=2):
    choice = random.choice(["sub", "obj", "reg", "proc", "lock"])

    if choice == "sub" and depth < max_depth:
        return generate_SUBLOGON_BLOCK(depth + 1, max_depth)

    elif choice == "obj":
        return generate_OBJECT_OP()

    elif choice == "reg":
        return generate_REGISTRY_OP()

    elif choice == "proc":
        return generate_PROCESS_OP()

    elif choice == "lock":
        return generate_LOCK_UNLOCK()

    # fallback (if max recursion reached)
    return []


def generate_SUBLOGON_BLOCK(depth, max_depth):
    events = []
    events.extend(generate_SUBLOGON())
    if depth < max_depth:
        events.extend(generate_ACTIONS(depth, max_depth))
    events.extend(generate_SUBLOGOFF())
    return events


def generate_SUBLOGON():
    return [random.choice(SUBLOGONS)]


def generate_SUBLOGOFF():
    return [random.choice(SUBLOGOFF)]


def generate_OBJECT_OP():
    return [random.choice(OBJECT_OPS)]


def generate_REGISTRY_OP():
    return [random.choice(REGISTRY_OPS)]


def generate_PROCESS_OP():
    if random.random() < 0.8:
        return PROCESS_OPS_GENERIC[:] 
    else:
        return PROCESS_OPS_CMD[:]      


def generate_LOCK_UNLOCK():
    return LOCK_UNLOCK_PAIR[:]


# -------------------------------------------------------------
# DEMO
# -------------------------------------------------------------
if __name__ == "__main__":
    seq = generate_SESSION()
    for e in seq:
        print(e)
