import os
import pm4py
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.visualization.petri_net import visualizer as pn_visualizer

LOG_PATH = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/smaller_script.xes"

OUTPUT_DIR = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/pictures"
OUTPUT_PNG = os.path.join(OUTPUT_DIR, "inductive_miner_infrequent_smaller.png")


def filter_noise(log, coverage=0.8):
    """
    Keep only the most frequent variants until the given coverage is reached.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filtered_log = variants_filter.filter_log_variants_percentage(log, percentage=coverage)
    return filtered_log


def main():
    # 1. Read XES log
    log = pm4py.read_xes(LOG_PATH)

    log = filter_noise(log, coverage=0.8)

    net, im, fm = pm4py.discover_petri_net_inductive(
        log,
        noise_threshold=0.01 #0.7
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
