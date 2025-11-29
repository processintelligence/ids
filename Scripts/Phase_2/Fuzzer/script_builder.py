from pathlib import Path

def build_powershell_script(command_strings, output_path):
    output_path = Path(output_path)
    script_content = "\n\n".join(command_strings)  
    output_path.write_text(script_content, encoding="utf-8")