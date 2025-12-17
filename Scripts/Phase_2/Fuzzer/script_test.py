from pathlib import Path
from action_to_command_mapper import map_actions_to_commands
from script_builder import build_powershell_script

actions = ["Interactive_Logon", "Start_Process", "Create_Object", "Create_Registry", "Logoff"]

command_strings = map_actions_to_commands(actions)

output_path = Path("script_test.ps1")

build_powershell_script(command_strings, output_path)

print(f"PowerShell script written to {output_path.resolve()}")
