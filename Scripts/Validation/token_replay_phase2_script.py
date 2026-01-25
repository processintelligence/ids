from Scripts.Validation.evaluation_metrics import *

# Compute fitness and precision scores for the phase 2 petri net

pmnl_path = r"Scripts/Phase_2/PetriNet/pnml/phase_2_benign.pnml"

real_xes = r"GeneratedFiles/csv_xes/phase_2_final.xes"

fitness = compute_fitness(pmnl_path, real_xes)

print("Fitness score:", fitness)

precision = compute_precison(pmnl_path, real_xes)

print("Precision score:", precision)

