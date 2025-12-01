from pathlib import Path

def build_powershell_script(command_strings, output_path): # TODO: hardcode path, maybe generated files?
    output_path = Path(output_path)
    
    # TODO: Start out with creating all files and registry keys from the delete list
    # TODO: And delete all files and registry keys from create list

    start_marker = [
        '$Path = "C:\\FuzzStarter.txt"',
        '"START" | Out-File -FilePath $Path -Force -Encoding ascii'
    ]

    end_marker = [
        '$Path = "C:\\FuzzEnder.txt"',
        '"END" | Out-File -FilePath $Path -Force -Encoding ascii'
    ]

    full_script = "\n\n".join(
        start_marker
        + command_strings
        + end_marker
    )

    output_path.write_text(full_script, encoding="utf-8")