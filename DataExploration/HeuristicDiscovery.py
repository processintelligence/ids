import os
import pm4py
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.visualization.petri_net import visualizer as pn_visualizer

LOG_PATH = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/smaller_script.xes"

# Make sure this is a *file*, not just a directory path
OUTPUT_DIR = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/pictures"
OUTPUT_PNG = os.path.join(OUTPUT_DIR, "heuristics_miner_smaller.png")


def filter_noise(log, coverage=0.8):
    # will create the directory if it does not exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filtered_log = variants_filter.filter_log_variants_percentage(log, percentage=coverage)
    return filtered_log


def main():
    # 1. Read XES log
    log = pm4py.read_xes(LOG_PATH)

    # 2. Remove infrequent variants / noise
    log = filter_noise(log, coverage=0.8)  # tweak 0.8 -> 0.7 / 0.9 as you like

    # 3. Discover Petri net with Heuristics Miner
    net, im, fm = pm4py.discover_petri_net_heuristics(
        log,
        dependency_threshold=0.9,
        and_threshold=0.8,
        loop_two_threshold=0.8,
    )

    # 4. Visualize and save Petri net
    gviz = pn_visualizer.apply(
        net,
        im,
        fm,
        log=log,
        variant=pn_visualizer.Variants.FREQUENCY,
        parameters={"format": "png"},
    )
    pn_visualizer.save(gviz, OUTPUT_PNG)
    pn_visualizer.view(gviz)


if __name__ == "__main__":
    main()
