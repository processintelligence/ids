import random
from pathlib import Path
import argparse
from Scripts.Phase_2.Fuzzer.action_generator import generate_SESSION
from Scripts.Phase_2.Fuzzer.action_to_command_mapper import map_actions_to_commands
from Scripts.Phase_2.Fuzzer.script_builder import build_powershell_script


def generate_n_scripts(n, seed):
    if seed is not None:
        random.seed(seed)
    output_path = "GeneratedFiles/PowershellScripts"
    output_dir = Path(output_path)
    output_dir.mkdir(exist_ok=True)

    for i in range(1, n + 1):
        actions = generate_SESSION()

        commands = map_actions_to_commands(actions)

        script_path = output_dir / f"script_{i:05d}.ps1"

        build_powershell_script(commands, script_path)

    print(f"\nGenerated {n} scripts in {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Powershell scripts for VM."
    )
    parser.add_argument("--n", required=True, type=int, help="Number of Powershell scripts.")
    parser.add_argument("--seed", default=None, help="Optional seed for random generator.")
    args = parser.parse_args()

    generate_n_scripts(args.n, args.seed)
