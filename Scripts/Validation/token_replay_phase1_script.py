from Scripts.Validation.evaluation_metrics import *

# Compute fitness and precision scores for the phase 1 petri net
# Since the petri net is designed by hand, we compute fitness with the real data from Los Alamos

pmnl_path = r"Scripts/Phase_1/pnml/phase_1_benign.pnml"

real_xes = r"LosAlamos/wls_800MB.xes"

fitness = compute_fitness(pmnl_path, real_xes)

print("Fitness score:", fitness)

precision = compute_precison(pmnl_path, real_xes)

print("Precision score:", precision)

