import os
import pm4py

from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


# =====================================================
# ================ CONFIGURATION ======================
# =====================================================

# --- Paths ---
LOG_PATH = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/smaller_script_clean_test.xes"

OUTPUT_DIR = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/PNML"
OUTPUT_PNG = os.path.join(OUTPUT_DIR, "inductive_test1.png")
OUTPUT_PNML = os.path.join(OUTPUT_DIR, "inductive_test1.pmnl")

APPLY_VARIANT_FILTERING = True
VARIANT_COVERAGE = 0.95

NOISE_THRESHOLD = 0.45


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


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Read XES log
    log = pm4py.read_xes(LOG_PATH)

    # 2. Optional variant-based filtering
    if APPLY_VARIANT_FILTERING:
        log = filter_noise(log, coverage=VARIANT_COVERAGE)

    # 3. Discover Petri net using Inductive Miner
    net, im, fm = pm4py.discover_petri_net_inductive(
        log,
        noise_threshold=NOISE_THRESHOLD
    )

    # 4. Export PNML
    pnml_exporter.apply(net, im, OUTPUT_PNML, final_marking=fm)

    # 5. Visualize and save Petri net
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
