import subprocess
import argparse
from pathlib import Path
import time


def run_powershell_script(script_path):
    try:
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
        )
        return result.returncode == 0

    except Exception:
        return False


def run_all_tests(delay):
    script_dir = "GeneratedFiles/PowershellScripts"
    directory = Path(script_dir)
    scripts = sorted(directory.glob("*.ps1"))

    if not scripts:
        print(f"No scripts found in: {directory}")
        return

    total = len(scripts)
    print(f"Running {total} PowerShell scripts from '{directory}'...")

    successes = 0

    for script in scripts:
        if run_powershell_script(script):
            successes += 1
        time.sleep(delay)

    print(f"Done. Successful: {successes}/{total}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--delay", type=float, default=0.5, help="Delay between runs (seconds)")
    args = parser.parse_args()

    run_all_tests(args.delay)


if __name__ == "__main__":
    main()
