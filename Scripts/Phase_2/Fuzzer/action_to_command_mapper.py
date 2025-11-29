from commands import (
    BatchLogonCommand,
    CreateObjectCommand,
    CreateRegistryCommand,
    DeleteObjectCommand,
    DeleteRegistryCommand,
    FailedLogonCommand,
    InteractiveLogonCommand,
    LogoffCommand,
    LockWorkstationCommand,
    ModifyObjectCommand,
    ModifyRegistryCommand,
    NetworkLogonCommand,
    RunAsLogonCommand,
    ServiceLogonCommand,
    StartCMDProcessCommand,
    StartProcessCommand
)

def map_action_to_command(action): # TODO: make private?
    mapping = {
        "Batch_Logon": BatchLogonCommand,
        "Create_Object": CreateObjectCommand,
        "Create_Registry": CreateRegistryCommand,
        "Delete_Object": DeleteObjectCommand,
        "Delete_Registry": DeleteRegistryCommand,
        "Failed_Logon": FailedLogonCommand,
        "Interactive_Logon": InteractiveLogonCommand,
        "Logoff": LogoffCommand,
        "Lock_Workstation": LockWorkstationCommand,
        "Modify_Object": ModifyObjectCommand,
        "Modify_Registry": ModifyRegistryCommand,
        "Network_Logon": NetworkLogonCommand,
        "RunAs_Logon": RunAsLogonCommand,
        "Service_Logon": ServiceLogonCommand,
        "Start_CMD_Process": StartCMDProcessCommand,
        "Start_Process": StartProcessCommand,
    }

    # TODO: Is exceptions for unknown actions needed? Should not be possible?

    return mapping[action]().getCommand()

def map_actions_to_commands(action_list):
    return [map_action_to_command(a) for a in action_list]


""" #MAPPER TEST
trace = ["Interactive_Logon", "Start_Process", "Create_Object", "Logoff"]

command_strings = map_actions_to_commands(trace)

for line in command_strings:
    print(line) """
