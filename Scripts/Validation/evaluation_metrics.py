import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay


def compute_precison(pmnl_path, xes_path):
    log = xes_importer.apply(xes_path)

    net, initial_marking, final_marking = pnml_importer.apply(pmnl_path)

    precision = precision_evaluator.apply(
        log,
        net,
        initial_marking,
        final_marking
    )
        
    return precision

def compute_fitness(pmnl_path, xes_path):
    log = xes_importer.apply(xes_path)

    net, initial_marking, final_marking = pnml_importer.apply(pmnl_path)

    results = token_replay.apply(log, net, initial_marking, final_marking)

    trace_fitnesses = [r["trace_fitness"] for r in results]
    average_fitness = sum(trace_fitnesses) / len(trace_fitnesses)
        
    return average_fitness
    



