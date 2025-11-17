from directly_follows import generate_translated_directly_follows
from directly_follows import log_normalize_directly_follows
from directly_follows import row_normalize_directly_follows
from plotting_util import plot_directly_follows_heatmap_3_col
from plotting_util import plot_directly_follows_heatmap_4_col
from plotting_util import diff_maps
from collections import defaultdict

xes_path_R = r"c:\Users\lomo0\Documents\RandomScripts\wls_800MB.xes"
xes_path_P = r"C:\Users\lomo0\Documents\GitHub\MasterRepo\MasterRepo\GeneratedFiles\WebPPL_XES\data_phase_1_net.xes"

directly_follows_P = generate_translated_directly_follows(xes_path_P)
directly_follows_R = generate_translated_directly_follows(xes_path_R)
directly_follows_R["4634_5"] = defaultdict(int)

log_normalize_P = log_normalize_directly_follows(directly_follows_P)
row_normalize_P = row_normalize_directly_follows(directly_follows_P)
plot_directly_follows_heatmap_4_col(log_normalize_P, "Log P directly follows heatmap")
plot_directly_follows_heatmap_4_col(row_normalize_P, "Row P directly follows heatmap")

log_normalize_R = log_normalize_directly_follows(directly_follows_R)
row_normalize_R = row_normalize_directly_follows(directly_follows_R)
plot_directly_follows_heatmap_4_col(log_normalize_R, "Log R directly follows heatmap")
plot_directly_follows_heatmap_4_col(row_normalize_R, "Row R directly follows heatmap")

""" RED: They have something we don't have
    GRE: We have the same ammount of something
    BLU: We have something they don't have"""

diff_row = diff_maps(row_normalize_R, row_normalize_P)
plot_directly_follows_heatmap_3_col(diff_row, "Row-normalized difference heatmap (R - P)")
