from Scripts.Validation.directly_follows import *
from Scripts.Validation.plotting_util import *
from collections import defaultdict


xes_path_P = "GeneratedFiles/WebPPL_XES/data_phase_1_benign.xes"
xes_path_R = "LosAlamos/wls_800MB.xes"

directly_follows_P = generate_translated_directly_follows(xes_path_P)
directly_follows_R = generate_translated_directly_follows(xes_path_R)

directly_follows_P["4634_3"] = defaultdict(int)
directly_follows_P["4634"] = defaultdict(int)

directly_follows_R["4634_5"] = defaultdict(int)


log_normalize_P = log_normalize_directly_follows(directly_follows_P)
row_normalize_P = row_normalize_directly_follows(directly_follows_P)

log_normalize_R = log_normalize_directly_follows(directly_follows_R)
row_normalize_R = row_normalize_directly_follows(directly_follows_R)

diff_row, black, white = diff_maps(row_normalize_R, row_normalize_P, verbose=True, threshold=10)

plot_dfg_heatmap(log_normalize_R, title="Log Normalized Los Alamos Dataset", color_scheme="3-band")
plot_dfg_heatmap(row_normalize_R, title="Row Normalized Los Alamos Dataset", color_scheme="3-band")

plot_dfg_heatmap(log_normalize_P, title="Log Normalized Phase 1", color_scheme="3-band")
plot_dfg_heatmap(row_normalize_P, title="Row Normalized Phase 1", color_scheme="3-band")


plot_dfg_heatmap(diff_row, title="Difference between Los Alamos and Phase 1", color_scheme="3-band", black_list=black, white_list=white)
