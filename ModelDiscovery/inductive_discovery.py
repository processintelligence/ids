import os
import pm4py
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter


LOG_PATH = "GeneratedFiles/csv_xes/smaller_script_prob_72_58_cor.xes"

OUTPUT_DIR_PNML = "GeneratedFiles/PNML"
OUTPUT_DIR_PNG = "GeneratedFiles/PNG"

NAME = "inductive_discovery_model"
OUTPUT_PNML = os.path.join(OUTPUT_DIR_PNML, NAME+".pnml")
OUTPUT_PNG = os.path.join(OUTPUT_DIR_PNG, NAME+".png")

APPLY_VARIANT_FILTERING = True
VARIANT_COVERAGE = 0.9

NOISE_THRESHOLD = 0.3


def filter_noise(log, coverage):
    return variants_filter.filter_log_variants_percentage(log, percentage=coverage)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR_PNML, exist_ok=True)
    os.makedirs(OUTPUT_DIR_PNG, exist_ok=True)

    log = pm4py.read_xes(LOG_PATH)

    if APPLY_VARIANT_FILTERING:
        log = filter_noise(log, coverage=VARIANT_COVERAGE)

    net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=NOISE_THRESHOLD)

    pnml_exporter.apply(net, im, OUTPUT_PNML, final_marking=fm)

    gviz = pn_visualizer.apply(net, im, fm, log=log, variant=pn_visualizer.Variants.FREQUENCY, parameters={"format": "png"})
    pn_visualizer.save(gviz, OUTPUT_PNG)
    pn_visualizer.view(gviz)