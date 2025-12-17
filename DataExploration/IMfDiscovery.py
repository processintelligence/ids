import os
import pm4py

from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.objects.process_tree.obj import ProcessTree
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.algo.filtering.log.variants import variants_filter


# =====================================================
# ================= CONFIGURATION =====================
# =====================================================

XES_FILE = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/smaller_script_clean_test.xes"

OUTPUT_DIR = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/PNML"
OUTPUT_PNG = os.path.join(OUTPUT_DIR, "IMf_test1.png")
OUTPUT_PNML = os.path.join(OUTPUT_DIR, "IMf_test1.pnml")

# ---------- Precision controls ----------
APPLY_VARIANT_FILTERING = True
VARIANT_COVERAGE = 0.7
NOISE_THRESHOLD = 0.25

#0.25, 0.25 = 0.95, 0.55
#0.25, 0.50 = 0.95, 0.55
#0.25, 0.90 = 0.95, 0.55
#0.10, 0.25 = 0.87, 1.00, Very bad petri net
#0.20, 0.25 = 0.98, 0.75, very bad petri net
#0.30, 0.25 = 0.94, 0.55
#0.40, 0.25 = 0.96, 0.53
#0.50, 0.25 = 0.98, 0.43
#0.70, 0.25 = 0.99, 0.33, maybe not that bed even though bad precision


# =====================================================
# =====================================================


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Import log
    log = xes_importer.apply(XES_FILE)
    print("Log imported")

    # 2. Variant-based filtering (critical for precision)
    if APPLY_VARIANT_FILTERING:
        log = variants_filter.filter_log_variants_percentage(
            log,
            percentage=VARIANT_COVERAGE
        )
        print(f"Variant filtering applied (coverage={VARIANT_COVERAGE})")

    # 3. Discover model using IMf (PROCESS TREE)
    parameters = {
        "noiseThreshold": NOISE_THRESHOLD
    }

    res = inductive_miner.apply(
        log,
        variant=inductive_miner.Variants.IMf,
        parameters=parameters
    )
    print("IMf model discovered")

    # 4. Convert Process Tree → Petri net
    if isinstance(res, ProcessTree):
        net, initial_marking, final_marking = pt_converter.apply(
            res,
            variant=pt_converter.Variants.TO_PETRI_NET
        )
    else:
        net, initial_marking, final_marking = res

    print("Petri net created")

    # 5. Export PNML
    pnml_exporter.apply(
        net,
        initial_marking,
        OUTPUT_PNML,
        final_marking=final_marking
    )

    # 6. Visualize and save PNG
    gviz = pn_visualizer.apply(
        net,
        initial_marking,
        final_marking
    )
    pn_visualizer.save(gviz, OUTPUT_PNG)

    print("Done")


if __name__ == "__main__":
    main()
