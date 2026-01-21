import random
from pathlib import Path
from Scripts.Phase_2.Fuzzer.pools.pool_access import *

FILES_PATH = "files.json"
PROCESSES_PATH = "processes.json"
REGISTRY_NAMES_PATH = "registry_names.json"
REGISTRY_VALUES_PATH = "registry_values.json"
TASKS_PATH = "tasks.json"
USERS_PATH = "users.json"
DELETE_MODIFY_FILES_PATH = "delete_modify_files.json"
DELETE_MODIFY_REGISTRY_PATH = "delete_modify_registry.json"
REGISTRY_KEY = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"


class Command:
    def getCommand(self):
        return self.command_string


class BatchLogonCommand(Command):
    def __init__(self):
        task_name = get_random_value(TASKS_PATH)
        self.command_string = f'Start-ScheduledTask -TaskName "{task_name}"'


class CreateObjectCommand(Command):
    def __init__(self):
        path = get_random_value(FILES_PATH)

        self.command_string = f'"Create" | Out-File "{path}"'


class DeleteObjectCommand(Command):
    def __init__(self):
        path = get_random_value(DELETE_MODIFY_FILES_PATH) 
        self.command_string = f'Remove-Item -Path "{path}" -Force'


class ModifyObjectCommand(Command):
    def __init__(self):
        path = get_random_value(DELETE_MODIFY_FILES_PATH)
        self.command_string = (
            f'Add-Content -Path "{path}" -Value "Modified"'
        )


class CreateRegistryCommand(Command):
    def __init__(self):
        key = REGISTRY_KEY
        name = get_random_value(REGISTRY_NAMES_PATH)
        value = get_random_value(REGISTRY_VALUES_PATH)
        self.command_string = (
            f'Set-ItemProperty -Path "{key}" -Name "{name}" -Value "{value}"'
        )


class DeleteRegistryCommand(Command):
    def __init__(self):
        key = REGISTRY_KEY
        name = get_random_value(DELETE_MODIFY_REGISTRY_PATH)
        self.command_string = (
            f'Remove-ItemProperty -Path "{key}" -Name "{name}"'
        )


class ModifyRegistryCommand(Command):
    def __init__(self):
        key = REGISTRY_KEY
        name = get_random_value(DELETE_MODIFY_REGISTRY_PATH)
        value = get_random_value(REGISTRY_VALUES_PATH)
        self.command_string = (
            f'Set-ItemProperty -Path "{key}" -Name "{name}" -Value "{value}"'
        )


class ModifyCommonRegistryCommand(Command):
    def __init__(self):
        key = REGISTRY_KEY
        name = "CommonDummy"
        value = get_random_value(REGISTRY_VALUES_PATH) + str(random.randint(1, 100000))
        self.command_string = (
            f'Set-ItemProperty -Path "{key}" -Name "{name}" -Value "{value}"'
        )


class FailedLogonCommand(Command):
    def __init__(self):
        user, correct_pass = get_random_key_value(USERS_PATH)
        wrong_pass = "Wrong"
        self.command_string = f"""
$secure = ConvertTo-SecureString "{wrong_pass}" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("{user}", $secure)

try {{
    Start-Process "cmd.exe" -Credential $cred -ErrorAction Stop
}}
catch {{
}}
""".strip()


class InteractiveLogonCommand(Command):
    def __init__(self):
        user, password = get_random_key_value(USERS_PATH)
        domain = "."
        self.command_string = f'''
$username = "{user}"
$domain = "{domain}"
$password = "{password}"

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class LogonUtil {{
    [DllImport("advapi32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
    public static extern bool LogonUser(
        string lpszUsername,
        string lpszDomain,
        string lpszPassword,
        int dwLogonType,
        int dwLogonProvider,
        out IntPtr phToken);
}}

public class HandleUtil {{
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool CloseHandle(IntPtr hObject);
}}
"@

$intertoken = [IntPtr]::Zero
[LogonUtil]::LogonUser($username, $domain, $password, 2, 0, [ref] $intertoken)
'''.strip()


class InteractiveLogoffCommand(Command):
    def __init__(self):
        self.command_string = '[HandleUtil]::CloseHandle($intertoken) | Out-Null'


class NetworkLogonCommand(Command):
    def __init__(self):
        user, password = get_random_key_value(USERS_PATH)
        domain = "."
        self.command_string = f'''
$username = "{user}"
$domain = "{domain}"
$password = "{password}"

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class LogonUtil {{
    [DllImport("advapi32.dll", SetLastError=true, CharSet=CharSet.Unicode)]
    public static extern bool LogonUser(
        string lpszUsername,
        string lpszDomain,
        string lpszPassword,
        int dwLogonType,
        int dwLogonProvider,
        out IntPtr phToken);
}}

public class HandleUtil {{
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool CloseHandle(IntPtr hObject);
}}
"@

$nettoken = [IntPtr]::Zero
[LogonUtil]::LogonUser($username, $domain, $password, 3, 0, [ref] $nettoken)
'''.strip()


class NetworkLogoffCommand(Command):
    def __init__(self):
        self.command_string = '[HandleUtil]::CloseHandle($nettoken) | Out-Null'


class RunAsLogonCommand(Command):
    def __init__(self):
        user, password = get_random_key_value(USERS_PATH)
        full_user = f"DESKTOP-40HV17C\\{user}"
        exe = "cmd.exe"
        self.command_string = f"""    
$RunAsCmd = "runas.exe /netonly /user:{full_user} `"{exe} /c exit`""
cmd.exe /c $RunAsCmd
Start-Sleep -Seconds 1
""".strip()


class StartCMDProcessCommand(Command):
    def __init__(self):
        self.command_string = 'Start-Process "cmd.exe"'


class StartProcessCommand(Command):
    def __init__(self):
        exe = get_random_value(PROCESSES_PATH)
        self.command_string = f'Start-Process -FilePath "{exe}"'
