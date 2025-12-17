from directly_follows import *
from plotting_util import *
from collections import defaultdict

#xes_path_R = r"c:\Users\lomo0\Documents\RandomScripts\wls_800MB.xes"
#xes_path_P = r"C:\Users\lomo0\Documents\GitHub\MasterRepo\MasterRepo\GeneratedFiles\WebPPL_XES\data_phase_1_net.xes"
xes_path_P = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/Personal/data_phase_1_20000.xes"
xes_path_R = "Personal/wls_800MB.xes"

directly_follows_P = generate_translated_directly_follows(xes_path_P)
directly_follows_R = generate_translated_directly_follows(xes_path_R)
directly_follows_R["4634_5"] = defaultdict(int)

log_normalize_P = log_normalize_directly_follows(directly_follows_P)
row_normalize_P = row_normalize_directly_follows(directly_follows_P)

log_normalize_R = log_normalize_directly_follows(directly_follows_R)
row_normalize_R = row_normalize_directly_follows(directly_follows_R)

diff_row, black, white = diff_maps(row_normalize_R, row_normalize_P, verbose=True, threshold=10)

plot_dfg_heatmap(diff_row, title="Diff Heatmap", color_scheme="4-band")
plot_dfg_heatmap(diff_row, title="Diff Heatmap", color_scheme="3-band")
plot_dfg_heatmap(diff_row, title="Diff Heatmap", color_scheme="3-band", black_list=black, white_list=white)
