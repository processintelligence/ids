import random


# -------------------------------------------------------------
# TERMINAL SYMBOLS
# -------------------------------------------------------------

SUCCESSFUL_MAIN_LOGONS = [
    "Interactive_Logon",
    "Network_Logon"
]

FAILED_LOGON = "Failed_Logon"

SUBLOGONS = [
    "Batch_Logon",
    "Service_Logon",
    "RunAs_Logon",
    "Network_Logon"
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
# PRODUCTION RULES
# -------------------------------------------------------------

def generate_SESSION():
    events = []
    events.extend(generate_MAIN_LOGON())
    return events


def generate_MAIN_LOGON():
    events = []

    # Generate 0–3 failed login attempts before success
    if random.random() < 0.25:
        failures = random.randint(1, 3)
        events.extend([FAILED_LOGON] * failures)

    # SUCCESSFUL_MAIN_LOGON
    main_logon_choice = random.choice(SUCCESSFUL_MAIN_LOGONS)
    events.append(main_logon_choice)
    if main_logon_choice == "Interactive_Logon":
        events.extend(generate_ACTIONS())
        events.extend(generate_MAIN_LOGOFF())

    return events


def generate_MAIN_LOGOFF():
    return [random.choice(LOGOFF)]


def generate_ACTIONS():
    events = []

    num_actions = random.randint(0, 4)

    for _ in range(num_actions):
        events.extend(generate_ACTION())

    return events


def generate_ACTION():
    ACTION = [
        "SUBLOGON",
        "OBJECT_OP",
        "REGISTRY_OP",
        "PROCESS_OP",
        "LOCK_UNLOCK"
    ]
    choice = random.choice(ACTION)

    if choice == "SUBLOGON":
        return generate_SUBLOGON()

    elif choice == "OBJECT_OP":
        return generate_OBJECT_OP()

    elif choice == "REGISTRY_OP":
        return generate_REGISTRY_OP()

    elif choice == "PROCESS_OP":
        return generate_PROCESS_OP()

    elif choice == "LOCK_UNLOCK":
        return generate_LOCK_UNLOCK()

    # if max recursion reached
    return []


def generate_SUBLOGON():
    events = []

    sublogin_choice = random.choice(SUBLOGONS)
    events.append(sublogin_choice)

    if sublogin_choice == "RunAs_Logon":
        events.extend(generate_ACTIONS())
        events.extend(generate_SUBLOGOFF())
    return events

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


""" #TEST
if __name__ == "__main__":
    seq = generate_SESSION()
    for e in seq:
        print(e) """
