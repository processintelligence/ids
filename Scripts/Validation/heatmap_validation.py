from directly_follows import *
from plotting_util import *
from collections import defaultdict

#xes_path_R = r"c:\Users\lomo0\Documents\RandomScripts\wls_800MB.xes"
#xes_path_P = r"C:\Users\lomo0\Documents\GitHub\MasterRepo\MasterRepo\GeneratedFiles\WebPPL_XES\data_phase_1_net.xes"
xes_path_P = "GeneratedFiles/WebPPL_XES/data_phase_1_net.xes"
xes_path_R = "Personal/wls_800MB.xes"

directly_follows_P = generate_translated_directly_follows(xes_path_P)
directly_follows_R = generate_translated_directly_follows(xes_path_R)
directly_follows_R["4634_5"] = defaultdict(int)

#log_normalize_P = log_normalize_directly_follows(directly_follows_P)
row_normalize_P = row_normalize_directly_follows(directly_follows_P)

#log_normalize_R = log_normalize_directly_follows(directly_follows_R)
row_normalize_R = row_normalize_directly_follows(directly_follows_R)

#plot_dfg_heatmap(log_normalize_P, "Log-normalized P directly-follows heatmap", "4-band", "nearest")
plot_dfg_heatmap(row_normalize_P, "Row-normalized P directly-follows heatmap", "4-band", "nearest")

#plot_dfg_heatmap(log_normalize_R, "Log-normalized R directly-follows heatmap", "4-band", "nearest")
plot_dfg_heatmap(row_normalize_R, "Row-normalized R directly-follows heatmap", "4-band", "nearest")

diff_row = diff_maps_bw(row_normalize_R, row_normalize_P)
plot_dfg_heatmap(diff_row, "Row-normalized difference heatmap (R - P)", "diff", "nearest")