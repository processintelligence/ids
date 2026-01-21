from Scripts.Phase_2.Fuzzer.commands import *

def map_action_to_command(action):
    mapping = {
        "Batch_Logon": BatchLogonCommand,
        "Create_Object": CreateObjectCommand,
        "Create_Registry": CreateRegistryCommand,
        "Delete_Object": DeleteObjectCommand,
        "Delete_Registry": DeleteRegistryCommand,
        "Failed_Logon": FailedLogonCommand,
        "Interactive_Logon": InteractiveLogonCommand,
        "Interactive_Logoff": InteractiveLogoffCommand,
        "Lock_Workstation": LockWorkstationCommand,
        "Unlock_Workstation": UnlockWorkstationCommand,
        "Modify_Object": ModifyObjectCommand,
        "Modify_Registry": ModifyRegistryCommand,
        "Modify_CommonStartup_Registry": ModifyCommonRegistryCommand,
        "Network_Logon": NetworkLogonCommand,
        "Network_Logoff": NetworkLogoffCommand,
        "RunAs_Logon": RunAsLogonCommand,
        "Service_Logon": ServiceLogonCommand,
        "Start_CMD_Process": StartCMDProcessCommand,
        "Start_Process": StartProcessCommand,
    }

    return mapping[action]().getCommand()

def map_actions_to_commands(action_list):
    return [map_action_to_command(a) for a in action_list]

