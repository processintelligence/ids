import random
from pathlib import Path
from pools.pool_access import getrandomfile, getrandomprocess, getrandomuserpass

class Command:
    def getCommand(self):
        return self.command_string


class BatchLogonCommand(Command):
    def __init__(self):
        task_name = "CMD Task" # TODO: Should this be randomized? And does it even matter?
        self.command_string = f'Start-ScheduledTask -TaskName "{task_name}"'


class CreateObjectCommand(Command):
    def __init__(self):
        #path = getrandomfile() UNCOMMENT
        # TODO: remove mock data
        path =  f"C:\Temp\FuzzFile{random.randint(1,100)}.txt"

        self.command_string = f'New-Item -Path "{path}" -ItemType File -Force | Out-Null'


class DeleteObjectCommand(Command):
    def __init__(self):
        # path = getrandomfile() TODO: Remove comment, special for delete?
        self.command_string = f'Remove-Item -Path "{path}" -Force'


class ModifyObjectCommand(Command):
    def __init__(self):
        # path = getrandomfile() TODO: Remove comment, special for modify?
        self.command_string = (
            f'Add-Content -Path "{path}" -Value "Modified at $(Get-Date)"'
        )


class CreateRegistryCommand(Command):
    def __init__(self):
        key = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" # TODO: getrandomregistrykey
        name = f"Test4657{random.randint(1,100)}"
        value = "abc"
        self.command_string = (
            f'Set-ItemProperty -Path "{key}" -Name "{name}" -Value "{value}"'
        )


class DeleteRegistryCommand(Command):
    def __init__(self):
        key = random_registry_key() # TODO: getrandomregistrykey (special for delete?)
        name = random_registry_name()
        self.command_string = (
            f'Remove-ItemProperty -Path "{key}" -Name "{name}"'
        )


class ModifyRegistryCommand(Command):
    def __init__(self):
        key = random_registry_key() # TODO: getrandomregistrykey (special for modify?)
        name = random_registry_name() # maybe key is always the same, but name and value is random
        value = random_registry_value()
        self.command_string = (
            f'Set-ItemProperty -Path "{key}" -Name "{name}" -Value "{value}"'
        )

# TODO: Should we add ModifyCommonStartupRegistryCommand?


class FailedLogonCommand(Command):
    def __init__(self):
        user, correct_pass = getrandomuserpass().split(":")
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
        user, password = getrandomuserpass().split(":")
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
"@

$token = [IntPtr]::Zero
[LogonUtil]::LogonUser($username, $domain, $password, 2, 0, [ref] $token) | Out-Null
'''.strip()

class LogoffCommand(Command):
    def __init__(self):
        self.command_string = '[System.Runtime.InteropServices.Marshal]::FreeHGlobal($token)'


class NetworkLogonCommand(Command):
    def __init__(self):
        user, password = getrandomuserpass().split(":")
        server = "10.0.2.15"
        self.command_string = (
            f'net use "\\\\{server}\\C$" /user:{user} {password}'
        )


class RunAsLogonCommand(Command): # TODO: Should we add as token login?
    def __init__(self):
        user, password = getrandomuserpass().split(":")
        full_user = f".\\{user}"
        exe = getrandomprocess()
        self.command_string = f"""
$RunAsCmd = "runas.exe /netonly /user:{full_user} `"{exe}`""
cmd.exe /c $RunAsCmd
""".strip()


class ServiceLogonCommand(Command): # TODO: Not sure this actually works
    def __init__(self):
        exe = getrandomprocess()
        service_name = "TempService4624" # TODO: Random service name?
        self.command_string = f"""
sc.exe create {service_name} binPath= "\\"{exe}\\"" obj= "NT AUTHORITY\\LocalService" type= own
Start-Service {service_name}
Start-Sleep -Seconds 2
Stop-Service {service_name} -Force
sc.exe delete {service_name}
""".strip()


class LockWorkstationCommand(Command):
    def __init__(self):
        self.command_string = "rundll32.exe user32.dll,LockWorkStation"


class UnlockWorkstationCommand(Command): # TODO: ?????
    def __init__(self):
        self.command_string = ""


class StartCMDProcessCommand(Command):
    def __init__(self):
        self.command_string = 'Start-Process "cmd.exe"'


class StartProcessCommand(Command):
    def __init__(self):
        exe = getrandomprocess()
        self.command_string = f'Start-Process -FilePath "{exe}"'
