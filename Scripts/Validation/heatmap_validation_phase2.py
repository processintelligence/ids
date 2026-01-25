from Scripts.Validation.directly_follows import *
from Scripts.Validation.plotting_util import *
from collections import defaultdict


xes_path_VM = "GeneratedFiles/csv_xes/phase_2_final.xes"
xes_path_simulated = "GeneratedFiles/WebPPL_XES/data_phase_2_benign.xes"

directly_follows_S = generate_translated_directly_follows_VM(xes_path_simulated)
directly_follows_VM = generate_translated_directly_follows_VM(xes_path_VM)

directly_follows_VM["4634_2"] = defaultdict(int)
directly_follows_S["4634_2"] = defaultdict(int)


log_normalize_S = log_normalize_directly_follows(directly_follows_S)
row_normalize_S = row_normalize_directly_follows(directly_follows_S)

log_normalize_VM = log_normalize_directly_follows(directly_follows_VM)
row_normalize_VM = row_normalize_directly_follows(directly_follows_VM)

diff_row, black, white = diff_maps(row_normalize_VM, row_normalize_S, verbose=True, threshold=1)

plot_dfg_heatmap(
    log_normalize_VM,
    title="Log Normalized VM",
    color_scheme="3-band"
)

plot_dfg_heatmap(
    row_normalize_VM,
    title="Row Normalized VM",
    color_scheme="3-band"
)

plot_dfg_heatmap(
    log_normalize_S,
    title="Log Normalized Phase 2",
    color_scheme="3-band"
)

plot_dfg_heatmap(
    row_normalize_S,
    title="Row Normalized Phase 2",
    color_scheme="3-band"
)

plot_dfg_heatmap(
    diff_row,
    title="Difference between VM and Phase 2",
    color_scheme="3-band",
    black_list=black,
    white_list=white,
    center_zero=True,
    symmetric_zero=True
)
