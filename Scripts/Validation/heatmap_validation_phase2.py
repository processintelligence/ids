from directly_follows import *
from plotting_util import *
from collections import defaultdict


xes_path_VM = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/combined_VM.xes"

directly_follows_VM = generate_translated_directly_follows_VM(xes_path_VM)

log_normalize_VM = log_normalize_directly_follows(directly_follows_VM)
row_normalize_VM = row_normalize_directly_follows(directly_follows_VM)

plot_dfg_heatmap(log_normalize_VM, title="Heatmap log normalized", color_scheme="3-band")
plot_dfg_heatmap(row_normalize_VM, title="Heatmap row normalized", color_scheme="3-band")
