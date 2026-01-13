from PetriNetUtil.PNMLToDataPNML import generate_config_structure
from PetriNetUtil.PNMLToDataPNML import generate_data_petrinet
from LogPPL.scripts.generate_uniform_traces import simulate_dpn
from Scripts.Validation.directly_follows import *
from Scripts.Validation.plotting_util import *
from Scripts.Phase_2.petrinet_cleaner import fix_transition_ids_inplace
from Scripts.Validation.evaluation_metrics import compute_precison, compute_fitness
import json


import os
import pm4py

from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

import itertools


APPLY_VARIANT_FILTERING = False

VARIANT_COVERAGE_VALUES = [0.0]
DEPENDENCY_VALUES = [0.5,0.8,0.99]
AND_VALUES = [0.5,0.8,0.99]
LOOP_TWO_VALUES = [0.5,0.8,0.99]


BEST_RESULT = {
    "fitness": -1,
    "precision": -1,
    "params": None
}



# =====================================================
# ================= CONFIGURATION =====================
# =====================================================

# --- Paths ---
LOG_PATH = r"C:\Users\lomo0\Downloads\900Rogue\smaller_script_rogue_fixed.xes"

OUTPUT_DIR = r"PNMLFiles\heuristic_test"
OUTPUT_PNG = os.path.join(OUTPUT_DIR, "h_rogue.png")
OUTPUT_PNML = os.path.join(OUTPUT_DIR, "h_rogue.pnml")


# =====================================================
# =====================================================


def filter_noise(log, coverage):
    """
    Keep only the most frequent variants until the given coverage is reached.
    """
    return variants_filter.filter_log_variants_percentage(
        log,
        percentage=coverage
    )

def fill_uniform_probabilities(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    arc_map = config.get("place_transition_arc", {})
    
    for place, arcs in arc_map.items():
        n = len(arcs)
        if n == 0:
            continue

        prob = 1.0 / n

        for arc in arcs:
            arcs[arc] = str(prob)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

def count_reachable_transitions(net):
    directly_follows = generate_translated_directly_follows_VM(net)
    
    print(directly_follows.items())

    print(f"Reachable transitions: {len(directly_follows.items())}")

    return len(directly_follows.items())


def run_pipeline(var_param, dep_param, and_param, loop_param,):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Read XES log
    log = pm4py.read_xes(LOG_PATH)

    # 2. Optional variant-based filtering
    if APPLY_VARIANT_FILTERING:
        log = filter_noise(log, coverage=var_param)

    # 3. Discover Petri net with Heuristics Miner
    net, im, fm = pm4py.discover_petri_net_heuristics(
        log,
        dependency_threshold=dep_param,
        and_threshold=and_param,
        loop_two_threshold=loop_param,
    )


    # 4. Export PNML
    pnml_exporter.apply(
        net,
        im,
        OUTPUT_PNML,
        final_marking=fm
    )

    # 5. Visualize and save PNG
    gviz = pn_visualizer.apply(
        net,
        im,
        fm,
        log=log,
        variant=pn_visualizer.Variants.FREQUENCY,
        parameters={"format": "png"},
    )
    pn_visualizer.save(gviz, OUTPUT_PNG)
    #pn_visualizer.view(gviz)

    # 


    # PMNL to simulate XES from
    #pnml_path = r"PNMLFiles\heuristic_test\h_actionprob.pnml"
    #pnml_path = r"C:\Users\lomo0\Downloads\XesNoConhost\IDHM_Prom.pnml"
    config_dir = r"Configs"

    fix_transition_ids_inplace(OUTPUT_PNML)

    config_path = generate_config_structure(OUTPUT_PNML, config_dir)

    fill_uniform_probabilities(config_path)
    print(f"Uniform config written to : {config_path}")

    data_pnml_path = generate_data_petrinet(config_path)
    print(f"Data PNML written to : {data_pnml_path}")

    steps = 15
    sample_size = 500
    simulate_dpn(steps=steps, sample_size=sample_size, pnml_path=data_pnml_path)
    print(f"Simulated {sample_size} traces of length {steps}")

    xes_dir = os.path.join("GeneratedFiles", "WebPPL_XES")
    os.makedirs(xes_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(data_pnml_path))[0]
    xes_path_model = os.path.abspath(os.path.join(xes_dir, f"{base_name}.xes"))

    reachable_transitions = count_reachable_transitions(xes_path_model)

    if reachable_transitions < 8:
        return -1, -1

    # EVAULUATION
    fitness = compute_fitness(OUTPUT_PNML, LOG_PATH)
    print(f"FITNESS: {fitness}")

    precision = compute_precison(OUTPUT_PNML, LOG_PATH)
    print(f"PRECISION: {precision}")

    return fitness, precision



if __name__ == "__main__":

    for var_param, dep_param, and_param, loop_param in itertools.product(
        VARIANT_COVERAGE_VALUES,
        DEPENDENCY_VALUES,
        AND_VALUES,
        LOOP_TWO_VALUES
    ):
        print(f"\nRunning: var={var_param}, dep={dep_param}, and={and_param}, loop={loop_param}")
        fitness, precision = run_pipeline(var_param, dep_param, and_param, loop_param)

        score = (fitness + precision) / 2

        if score > (BEST_RESULT["fitness"] + BEST_RESULT["precision"]) / 2:
            BEST_RESULT["fitness"] = fitness
            BEST_RESULT["precision"] = precision
            BEST_RESULT["params"] = (var_param, dep_param, and_param, loop_param)

    print("\n================ BEST RESULT ================")
    print(f"Params (dep, and, loop): {BEST_RESULT['params']}")
    print(f"Fitness: {BEST_RESULT['fitness']}")
    print(f"Precision: {BEST_RESULT['precision']}")






