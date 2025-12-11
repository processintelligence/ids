from directly_follows import *
from plotting_util import *
from collections import defaultdict


xes_path_VM = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/combined_VM_nodup.xes"
xes_path_phase1 = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/smaller_script.xes"
xes_path_model = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/WebPPL_XES/data_phase_2_net.xes"

#directly_follows_VM = generate_translated_directly_follows_VM(xes_path_VM)
#directly_follows_model = generate_translated_directly_follows_VM(xes_path_model)
directly_follows_phase1 = generate_translated_directly_follows_VM(xes_path_phase1)

#log_normalize_VM = log_normalize_directly_follows(directly_follows_VM)
#row_normalize_VM = row_normalize_directly_follows(directly_follows_VM)

#log_normalize_model = log_normalize_directly_follows(directly_follows_model)
#row_normalize_model = row_normalize_directly_follows(directly_follows_model)

log_normalize_phase1 = log_normalize_directly_follows(directly_follows_phase1)
row_normalize_phase1 = row_normalize_directly_follows(directly_follows_phase1)

#plot_dfg_heatmap(log_normalize_VM, title="Heatmap log normalized", color_scheme="3-band")
#plot_dfg_heatmap(row_normalize_VM, title="Heatmap row normalized", color_scheme="3-band")

#plot_dfg_heatmap(log_normalize_model, title="Heatmap log normalized", color_scheme="3-band")
#plot_dfg_heatmap(row_normalize_model, title="Heatmap row normalized", color_scheme="3-band")

plot_dfg_heatmap(log_normalize_phase1, title="Heatmap log normalized", color_scheme="3-band")
plot_dfg_heatmap(row_normalize_phase1, title="Heatmap row normalized", color_scheme="3-band")
