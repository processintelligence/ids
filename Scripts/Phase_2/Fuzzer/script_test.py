# simple_script_builder.py
from pathlib import Path
from action_to_command_mapper import map_actions_to_commands
from script_builder import build_powershell_script

# 1. Define your trace
actions = ["Interactive_Logon", "Start_Process", "Create_Object", "Create_Registry", "Logoff"]

# 2. Map the trace to PowerShell command stringsa
command_strings = map_actions_to_commands(actions)

# 3. Specify output path
output_path = Path("script_test.ps1")

# 4. Build the PowerShell script
build_powershell_script(command_strings, output_path)

print(f"PowerShell script written to {output_path.resolve()}")
