from Scripts.Simulation.pnml_to_data_pnml import generate_config_structure
from Scripts.Simulation.pnml_to_data_pnml import generate_data_petrinet
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

# All parameters that will be tried in the discovery pipeline

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


LOG_PATH = "GeneratedFiles/csv_xes/phase_2_final.xes"

OUTPUT_DIR_PNML = "GeneratedFiles/PNML"
OUTPIT_DIR_PNG = "GeneratedFiles/PNG"

OUTPUT_PNG = os.path.join(OUTPIT_DIR_PNG, "best_discovered_model.png")
OUTPUT_PNML = os.path.join(OUTPUT_DIR_PNML, "best_discovered_model.pnml")


def filter_noise(log, coverage):
    return variants_filter.filter_log_variants_percentage(
        log,
        percentage=coverage
    )

# Insert equal probabilities in all outgoing arcs from a place to allow simulation
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


# Count reachable transitions to ensure most events are reachable
def count_reachable_transitions(net):
    directly_follows = generate_translated_directly_follows_VM(net)
    
    print(directly_follows.items())

    print(f"Reachable transitions: {len(directly_follows.items())}")

    return len(directly_follows.items())

# For each parameter combination, discover model and compute conformance metrics
def run_pipeline(var_param, dep_param, and_param, loop_param,):
    os.makedirs(OUTPUT_DIR_PNML, exist_ok=True)

    log = pm4py.read_xes(LOG_PATH)

    if APPLY_VARIANT_FILTERING:
        log = filter_noise(log, coverage=var_param)

    net, im, fm = pm4py.discover_petri_net_heuristics(
        log,
        dependency_threshold=dep_param,
        and_threshold=and_param,
        loop_two_threshold=loop_param,
    )

    pnml_exporter.apply(
        net,
        im,
        OUTPUT_PNML,
        final_marking=fm
    )

    gviz = pn_visualizer.apply(
        net,
        im,
        fm,
        log=log,
        variant=pn_visualizer.Variants.FREQUENCY,
        parameters={"format": "png"},
    )
    pn_visualizer.save(gviz, OUTPUT_PNG)


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

    # Discover models with all possible parameter combinations and find the best one
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






