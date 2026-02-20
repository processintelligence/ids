from Scripts.Simulation.pnml_to_data_pnml import generate_config_structure
from Scripts.Simulation.pnml_to_data_pnml import generate_data_petrinet
from LogPPL.scripts.generate_uniform_traces import simulate_dpn
from Scripts.Validation.directly_follows import *
from Scripts.Validation.plotting_util import *
from Scripts.Phase_2.petrinet_cleaner import fix_transition_ids_inplace
from Scripts.Validation.evaluation_metrics import compute_precision, compute_fitness
import json

# Insert equal probabilities in all outgoing arcs from a place to allow simulation
def fill_uniform_probabilities(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    arc_map = config.get("place_transition_arc", {})

    for place, arcs in arc_map.items():
        n = len(arcs)
        if n == 0:
            continue

        prob = 1.0 / n

        for arc in arcs:
            arcs[arc] = str(prob)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

# PIPELINE

xes_path_scripts = "GeneratedFiles/csv_xes/phase_2_final.xes"
pnml_path = "Scripts/Phase_2/PetriNet/pnml/phase_2_benign.pnml"

config_dir = r"Configs"

fix_transition_ids_inplace(pnml_path)

config_path = generate_config_structure(pnml_path, config_dir)

fill_uniform_probabilities(config_path)
print(f"Uniform config written to : {config_path}")

data_pnml_path = generate_data_petrinet(config_path)
print(f"Data PNML written to : {data_pnml_path}")

steps = 25
sample_size = 5000
simulate_dpn(steps=steps, sample_size=sample_size, pnml_path=data_pnml_path)
print(f"Simulated {sample_size} traces of length {steps}")

xes_dir = os.path.join("GeneratedFiles", "WebPPL_XES")
os.makedirs(xes_dir, exist_ok=True)
base_name = os.path.splitext(os.path.basename(data_pnml_path))[0]
xes_path_model = os.path.abspath(os.path.join(xes_dir, f"{base_name}.xes"))

# EVAULUATION
fitness = compute_fitness(pnml_path, xes_path_scripts)
print(f"FITNESS: {fitness}")

precision = compute_precision(pnml_path, xes_path_scripts)
print(f"PRECISION: {precision}")

# Heatmaps
directly_follows_model = generate_translated_directly_follows_VM(xes_path_model)
directly_follows_scripts = generate_translated_directly_follows_VM(xes_path_scripts)

directly_follows_scripts["4634_2"] = defaultdict(int)
directly_follows_model["4634_2"] = defaultdict(int)

log_normalize_model = log_normalize_directly_follows(directly_follows_model)
row_normalize_model = row_normalize_directly_follows(directly_follows_model)

log_normalize_scripts = log_normalize_directly_follows(directly_follows_scripts)
row_normalize_scripts = row_normalize_directly_follows(directly_follows_scripts)

diff_row, black, white = diff_maps(row_normalize_scripts, row_normalize_model, verbose=True, threshold=10)

print("black")
print(black, len(black))

print("white")
print(white, len(white))


plot_dfg_heatmap(log_normalize_model, title="Log Normalized - Model", color_scheme="3-band")
plot_dfg_heatmap(row_normalize_model, title="Row Normalized - Model", color_scheme="3-band")

plot_dfg_heatmap(log_normalize_scripts, title="Log Normalized - Scripts", color_scheme="3-band")
plot_dfg_heatmap(row_normalize_scripts, title="Row Normalized - Scripts", color_scheme="3-band")

plot_dfg_heatmap(diff_row, title="Diff Heatmap", color_scheme="3-band", black_list=black, white_list=white)