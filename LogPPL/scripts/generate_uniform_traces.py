#Usage (from repository root):
#python -m scripts.generate_uniform_traces --pnml examples/data/newtry.pnml --sim_steps 10 --samples 10 --run-webppl

import argparse
import os

from LogPPL.pnml_to_webppl.dpn import DPN
from LogPPL.pnml_to_webppl.converter import convert_dpn_to_webPPL
from LogPPL.pnml_to_webppl.functions.create_log import find_npm_global_path, generate_event_log

# Set up uniform distributions for all variables in all transitions
def build_uniform_distributions(dpn):
    distributions = {}

    transitions = [t.name for t in dpn.net.transitions]
    variables = list(dpn.variable_information.keys())

    for t in transitions:
        distributions[t] = {}
        for v in variables:
            distributions[t][v] = "globalStore.{write_variable} = uniform({{a: 0, b: 1}});"

    return distributions

def simulate_dpn(steps, sample_size, pnml_path):
    pnml_path = os.path.abspath(pnml_path) # Assume absolute path
    if not os.path.exists(pnml_path):
        print(f"PNML file not found: {pnml_path}")
        return

    webppl_dir = "GeneratedFiles\WebPPL"
    os.makedirs(webppl_dir, exist_ok=True)
    xes_dir = "GeneratedFiles\WebPPL_XES"
    os.makedirs(xes_dir, exist_ok=True)

    dpn_preview = DPN(pnml_path, distributions={})

    distributions = build_uniform_distributions(dpn_preview)

    print("Converting PNML to WebPPL")

    webppl_code = convert_dpn_to_webPPL(pnml_path, verbose=True, simulation_steps=steps,
                                       sample_size=sample_size, simulation_query="false", distributions=distributions)

    base_name = os.path.splitext(os.path.basename(pnml_path))[0]
    wppl_path = os.path.abspath(os.path.join(webppl_dir, f"{base_name}.wppl"))
    with open(wppl_path, "w", encoding="utf-8") as f:
        f.write(webppl_code)

    print(f"Saved WebPPL to: {wppl_path}")

    print("Looking for webppl executable...")
    webppl_exec = find_npm_global_path()
    if webppl_exec is None or not os.path.exists(webppl_exec):
        print("webppl executable not found. Install webppl globally (npm i -g webppl)")
        print(wppl_path)
        return

    print(f"Running webppl ({webppl_exec}) to generate XES log. This may take a while...")
    try:
        xes_str = generate_event_log(webppl_exec, wppl_path)
        xes_path = os.path.abspath(os.path.join(xes_dir, f"{base_name}.xes"))
        with open(xes_path, "w", encoding="utf-8") as f:
            f.write(xes_str)
        print(f"Saved XES to: {xes_path}")
    except Exception as e:
        print(f"Error running webppl: {e}")

"""     # TODO: delete main
def main():
    parser = argparse.ArgumentParser(description="Convert PNML -> WebPPL using uniform(0,1) for all variables")
    parser.add_argument("--pnml", required=True, help="Path to PNML (.pnml) file")
    parser.add_argument("--out-dir", default="generated", help="Output directory for .wppl and .xes files")
    parser.add_argument("--sim_steps", type=int, default=50, help="Simulator loops / steps used in converter")
    parser.add_argument("--samples", type=int, default=500, help="Sample size used in converter")
    parser.add_argument("--run-webppl", action="store_true", help="Attempt to run webppl and produce XES (requires webppl installed)")

    args = parser.parse_args()

    pnml_path = os.path.abspath(args.pnml)
    if not os.path.exists(pnml_path):
        print(f"PNML file not found: {pnml_path}")
        return
    webppl_dir = "GeneratedFiles\WebPPL"
    os.makedirs(webppl_dir, exist_ok=True)

    # Build a temporary DPN to inspect variables/transitions
    dpn_preview = DPN(pnml_path, distributions={})

    # Build uniform distributions and pass them into the converter
    distributions = build_uniform_distributions(dpn_preview)

    print("Converting PNML -> WebPPL (using uniform(0,1) for all variables)...")

    # Use a safe default for simulation_query: when empty, pass 'false' so the generated
    # WebPPL doesn't contain an invalid `if ()` check.
    simulation_query = "false"
    webppl_code = convert_dpn_to_webPPL(pnml_path, verbose=True, simulation_steps=args.sim_steps,
                                       sample_size=args.samples, simulation_query=simulation_query, distributions=distributions)

    base_name = os.path.splitext(os.path.basename(pnml_path))[0]
    wppl_path = os.path.abspath(os.path.join(webppl_dir, f"{base_name}.wppl"))
    with open(wppl_path, "w", encoding="utf-8") as f:
        f.write(webppl_code)

    print(f"Saved WebPPL to: {wppl_path}")

    if args.run_webppl:
        print("Looking for webppl executable (npm global) ...")
        webppl_exec = find_npm_global_path()
        if webppl_exec is None or not os.path.exists(webppl_exec):
            print("webppl executable not found. Install webppl globally (npm i -g webppl) or run the wppl file manually:")
            print(wppl_path)
            return

        print(f"Running webppl ({webppl_exec}) to generate XES log. This may take a while...")
        try:
            xes_dir = "GeneratedFiles\WebPPL_XES"
            xes_str = generate_event_log(webppl_exec, wppl_path)
            xes_path = os.path.abspath(os.path.join(xes_dir, f"{base_name}.xes"))
            with open(xes_path, "w", encoding="utf-8") as f:
                f.write(xes_str)
            print(f"Saved XES to: {xes_path}")
        except Exception as e:
            print(f"Error running webppl: {e}")
            print("If webppl cannot be run here, you can run it manually using:")
            print(f"webppl {wppl_path} > output.xes")

    else:
        print("To generate traces, run WebPPL manually or re-run with --run-webppl (requires webppl installed).")


if __name__ == "__main__":
    main()
 """