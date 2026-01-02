import os
import pm4py

from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.algo.discovery.heuristics.variants import plusplus as hm_plusplus
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


# =====================================================
# ================= CONFIGURATION =====================
# =====================================================

# --- Paths ---
LOG_PATH = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/smaller_script_clean_test.xes"

OUTPUT_DIR = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/PNML"
OUTPUT_PNG = os.path.join(OUTPUT_DIR, "heuristics_test1.png")
OUTPUT_PNML = os.path.join(OUTPUT_DIR, "heuristics_test1.pnml")

# --- Variant filtering ---
APPLY_VARIANT_FILTERING = True
VARIANT_COVERAGE = 0.9  # keep high if you want to preserve rare activities

# --- Heuristics Miner++ parameters (PM4Py names) ---
# These correspond to hm_plusplus.Parameters.* in PM4Py docs/source. :contentReference[oaicite:1]{index=1}
DEPENDENCY_THRESH = 0.75        # not 0.90 (keeps enough structure for fitness)
AND_MEASURE_THRESH = 0.85       # keep strict-ish parallelism, but not extreme
MIN_ACT_COUNT = 5               # drop ultra-rare activities that otherwise go dead
MIN_DFG_OCCURRENCES = 5         # don’t cut too many relations; tune with log size

HEU_NET_DECORATION = "frequency"  # "frequency" (safe) or "performance" if you rely on timestamps

#0.9, 0.75, 0.85, 5, 5 = 

# =====================================================

def filter_noise(log, coverage: float):
    """
    Keep only the most frequent variants until the given coverage is reached.
    """
    return variants_filter.filter_log_variants_percentage(log, percentage=coverage)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1) Read log
    log = pm4py.read_xes(LOG_PATH)

    # 2) Optional variant filtering
    if APPLY_VARIANT_FILTERING:
        log = filter_noise(log, coverage=VARIANT_COVERAGE)

    # 3) Discover Petri net with Heuristics Miner++
    parameters = {
        hm_plusplus.Parameters.DEPENDENCY_THRESH: DEPENDENCY_THRESH,
        hm_plusplus.Parameters.AND_MEASURE_THRESH: AND_MEASURE_THRESH,
        hm_plusplus.Parameters.MIN_ACT_COUNT: MIN_ACT_COUNT,
        hm_plusplus.Parameters.MIN_DFG_OCCURRENCES: MIN_DFG_OCCURRENCES,
        hm_plusplus.Parameters.HEU_NET_DECORATION: HEU_NET_DECORATION,
    }

    net, im, fm = hm_plusplus.apply(log, parameters=parameters)

    # 4) Export PNML
    pnml_exporter.apply(net, im, OUTPUT_PNML, final_marking=fm)

    # 5) Visualize & save PNG
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
