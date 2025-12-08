from pathlib import Path
from Scripts.Phase_2.Fuzzer.pools.pool_access import get_all_values


def build_powershell_script(command_strings, output_path): # TODO: hardcode path, maybe generated files?
    output_path = Path(output_path)
        
    all_delete_file = get_all_values("files.json")
    all_create_file = get_all_values("delete_modify_files.json")
    all_delete_registry = get_all_values("registry_names.json")
    all_create_registry = get_all_values("delete_modify_registry.json")

    cleanup = []

    for file in all_delete_file:
        command = f'if (!(Test-Path "{file}")) {{ New-Item -ItemType File -Path "{file}" -Force | Out-Null }}'
        cleanup.append(command)

    for file in all_create_file:
        command = f'if (Test-Path "{file}") {{ Remove-Item "{file}" -Force -Recurse }}'
        cleanup.append(command)

    for registry in all_delete_registry:
        command = f'Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "{registry}"'
        cleanup.append(command)


    for registry in all_create_registry:
        command = f'Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "{registry}" -Value "abc"'
        cleanup.append(command)


    start_marker = [
        '$Path = "C:\\Temp\\FuzzStarter.txt"',
        '"START" | Out-File -FilePath $Path -Force -Encoding ascii'
    ]

    end_marker = [
        '$Path = "C:\\Temp\\FuzzEnder.txt"',
        '"END" | Out-File -FilePath $Path -Force -Encoding ascii'
    ]

    full_script = "\n\n".join(
        cleanup
        + start_marker
        + command_strings
        + end_marker
    )

    output_path.write_text(full_script, encoding="utf-8")