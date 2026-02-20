import os
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.objects.conversion.process_tree import converter as pt_converter
from pm4py.objects.process_tree.obj import ProcessTree
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.algo.filtering.log.variants import variants_filter


LOG_PATH = "GeneratedFiles/csv_xes/full_vm_log.xes"

OUTPUT_DIR_PNML = "GeneratedFiles/PNML"
OUTPUT_DIR_PNG = "GeneratedFiles/PNG"

NAME = "imf_discovery_model"
OUTPUT_PNML = os.path.join(OUTPUT_DIR_PNML, NAME+".pnml")
OUTPUT_PNG = os.path.join(OUTPUT_DIR_PNG, NAME+".png")

APPLY_VARIANT_FILTERING = True
VARIANT_COVERAGE = 0.9
NOISE_THRESHOLD = 0.1


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR_PNML, exist_ok=True)
    os.makedirs(OUTPUT_DIR_PNG, exist_ok=True)

    log = xes_importer.apply(LOG_PATH)

    if APPLY_VARIANT_FILTERING:
        log = variants_filter.filter_log_variants_percentage(log, percentage=VARIANT_COVERAGE)


    parameters = {
        "noiseThreshold": NOISE_THRESHOLD
    }

    res = inductive_miner.apply(log, variant=inductive_miner.Variants.IMf, parameters=parameters)
    
    if isinstance(res, ProcessTree):
        net, initial_marking, final_marking = pt_converter.apply(res, variant=pt_converter.Variants.TO_PETRI_NET)
    else:
        net, initial_marking, final_marking = res

    pnml_exporter.apply(net, initial_marking, OUTPUT_PNML, final_marking=final_marking)

    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.save(gviz, OUTPUT_PNG)