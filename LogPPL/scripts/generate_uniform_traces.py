#TODO: Create copyright thing 

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

def simulate_dpn(steps, sample_size, pnml_path, attacktype=None):
    pnml_path = os.path.abspath(pnml_path)
    if not os.path.exists(pnml_path):
        print(f"PNML file not found: {pnml_path}")
        return

    webppl_dir = os.path.join("GeneratedFiles", "WebPPL")
    os.makedirs(webppl_dir, exist_ok=True)

    xes_dir = os.path.join("GeneratedFiles", "WebPPL_XES")
    os.makedirs(xes_dir, exist_ok=True)

    dpn_preview = DPN(pnml_path, distributions={})
    distributions = build_uniform_distributions(dpn_preview)

    # Convert to WebPPL
    print("Converting PNML to WebPPL")

    webppl_code = convert_dpn_to_webPPL(
        pnml_path,
        verbose=True,
        simulation_steps=steps,
        sample_size=sample_size,
        simulation_query="false",
        distributions=distributions,
        attacktype=attacktype
    )

    base_name = os.path.splitext(os.path.basename(pnml_path))[0]
    wppl_path = os.path.abspath(os.path.join(webppl_dir, f"{base_name}.wppl"))
    with open(wppl_path, "w", encoding="utf-8") as f:
        f.write(webppl_code)

    print(f"Saved WebPPL to: {wppl_path}")


    #Run WebPPL and generate XES
    webppl_exec = find_npm_global_path()
    if webppl_exec is None or not os.path.exists(webppl_exec):
        print("webppl executable not found")
        return
    
    print(f"Running webppl ({webppl_exec})")
    try:
        xes_str = generate_event_log(webppl_exec, wppl_path)
        xes_path = os.path.abspath(os.path.join(xes_dir, f"{base_name}.xes"))
        with open(xes_path, "w", encoding="utf-8") as f:
            f.write(xes_str)
        print(f"Saved XES to: {xes_path}")
    except Exception as e:
        print(f"Error running webppl: {e}")

    return xes_path
