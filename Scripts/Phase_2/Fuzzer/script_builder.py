from pathlib import Path
from Scripts.Phase_2.Fuzzer.pools.pool_access import get_all_values


def build_powershell_script(command_strings, output_path): # TODO: hardcode path, maybe generated files?
    output_path = Path(output_path)
        
    all_delete = get_all_values("files.json")
    all_create = get_all_values("delete_modify_files.json")

    cleanup = []

    for file in all_create:
        command = f'if (!(Test-Path "{file}")) {{ New-Item -ItemType File -Path "{file}" -Force | Out-Null }}'
        cleanup.append(command)

    for file in all_delete:
        command = f'if (Test-Path "{file}") {{ Remove-Item "{file}" -Force -Recurse }}'
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