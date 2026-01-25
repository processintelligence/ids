import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import random
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# Predefined colorschemes
COLOR_SCHEMES = {
    "3-band": [
        (0.00, "navy"),
        (0.33, "deepskyblue"),
        (0.34, "green"),
        (0.66, "lime"),
        (0.67, "orangered"),
        (1.00, "darkred"),
    ],
    "4-band": [
        (0.00, "navy"),
        (0.25, "deepskyblue"),
        (0.26, "green"),
        (0.50, "lime"),
        (0.51, "yellow"),
        (0.75, "gold"),
        (0.76, "orangered"),
        (1.00, "darkred"),
    ]
}

def get_colormap(scheme_name):
    # Validate scheme name
    if scheme_name not in COLOR_SCHEMES:
        raise ValueError(f"Unknown color scheme '{scheme_name}'. "
                         f"Available: {list(COLOR_SCHEMES.keys())}")
    return LinearSegmentedColormap.from_list(
        f"dfg_{scheme_name}",
        COLOR_SCHEMES[scheme_name]
    )

def nested_map_to_matrix(nested_map):
    # Convert a nested mapping into matrix
    # stable ordering of activities
    labels = sorted(nested_map.keys())                
    idx = {lab: i for i, lab in enumerate(labels)}
    n = len(labels)

    mat = np.zeros((n, n), dtype=float)             
    for src, inner in nested_map.items():
        i = idx[src]
        for dst, value in inner.items():
            if dst in idx:
                mat[i, idx[dst]] = float(value or 0)  

    return mat, labels, idx


def plot_dfg_heatmap(
    nested_map,
    title="Directly-Follows Heatmap",
    black_list=None,
    white_list=None,
    color_scheme="4-band",
    interpolation="nearest",
    figsize_scale=0.3,
    center_zero=False,
    symmetric_zero=False,
    vmin=None,
    vmax=None
):
    # black_list/white_list to overlay specific squares with black and white color
    black_list = black_list or []
    white_list = white_list or []

    mat, labels, idx = nested_map_to_matrix(nested_map)
    n = len(labels)

    cmap = get_colormap(color_scheme)         

    norm = None
    if center_zero:
        # Compute automatic min/max from matrix
        auto_min = float(np.nanmin(mat))
        auto_max = float(np.nanmax(mat))

        # Allow manual override of vmin/vmax
        _vmin = auto_min if vmin is None else float(vmin)
        _vmax = auto_max if vmax is None else float(vmax)

        # make limits symmetric around 0
        if symmetric_zero:
            L = max(abs(_vmin), abs(_vmax))
            _vmin, _vmax = -L, L

        # TwoSlopeNorm centers the colormap at 0.0
        norm = TwoSlopeNorm(vmin=_vmin, vcenter=0.0, vmax=_vmax)

    # Figure size scales with number of labels so ticks remain readable
    fig, ax = plt.subplots(
        figsize=(1.0 + figsize_scale * n, 1.0 + figsize_scale * n)
    )

    im = ax.imshow(mat, cmap=cmap, norm=norm, interpolation=interpolation)

    ax.set_xticks(range(n), labels=labels, rotation=90, fontsize=8)
    ax.set_yticks(range(n), labels=labels, fontsize=8)
    ax.set_xlabel("follows → (destination)")
    ax.set_ylabel("source")
    ax.set_title(title)

    # Draw grid lines between cells using ticks at half-integers
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle="-", linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("count", rotation=270, labelpad=12)

    # Overlay black cells for pairs in black_list
    for src, dst in black_list:
        if src in idx and dst in idx:
            i = idx[src]  # row index
            j = idx[dst]  # col index
            ax.add_patch(
                patches.Rectangle(
                    (j - 0.5, i - 0.5), 
                    1, 1,              
                    facecolor="black",
                    edgecolor="black",
                    linewidth=1
                )
            )

    # Overlay white cells for pairs in white_list
    for src, dst in white_list:
        if src in idx and dst in idx:
            i = idx[src]
            j = idx[dst]
            ax.add_patch(
                patches.Rectangle(
                    (j - 0.5, i - 0.5),
                    1, 1,
                    facecolor="white",
                    edgecolor="black",
                    linewidth=1
                )
            )

    plt.tight_layout()  
    plt.show()   



def diff_maps(mapA, mapB, verbose=False, threshold=0):
    # Compute element-wise difference (A - B) for two nested maps and also derive overlays.
    black_list, white_list = find_black_white(mapA, mapB, threshold=threshold)

    diff = {}

    # union of sources
    all_srcs = set(mapA.keys()) | set(mapB.keys())  

    for src in all_srcs:
        diff[src] = {}

        # union of destinations
        dsts = set(mapA.get(src, {}).keys()) | set(mapB.get(src, {}).keys())  

        for dst in dsts:
            # default missing edges to 0
            a = mapA.get(src, {}).get(dst, 0.0)      
            b = mapB.get(src, {}).get(dst, 0.0)
            result = a - b
            diff[src][dst] = result

            if verbose:
                print(f"{src} -> {dst}: {a} - {b} = {result}")

    return diff, black_list, white_list

def find_black_white(mapA, mapB, threshold=0):
    black_list = []
    white_list = []

    # union of sources
    all_srcs = set(mapA.keys()) | set(mapB.keys())  

    for src in all_srcs:
        dsts = set(mapA.get(src, {}).keys()) | set(mapB.get(src, {}).keys())
        for dst in dsts:
            a = mapA.get(src, {}).get(dst, 0.0)
            b = mapB.get(src, {}).get(dst, 0.0)

            # Present in A above threshold, absent in B
            if a > threshold and b == 0:
                black_list.append((src, dst))

            # Absent in A, present in B above threshold
            if a == 0 and b > threshold:
                white_list.append((src, dst))

    return black_list, white_list


def generate_random_directly_follows_data(n=20, min_val=0, max_val=20, seed=42):
    # Generate random data for testing purpose 
    random.seed(seed)
    labels = [f"Act_{i:02d}" for i in range(1, n + 1)]  
    data = {}
    for src in labels:
        inner = {}
        for dst in labels:
            inner[dst] = 0 if src == dst else random.randint(min_val, max_val)  
        data[src] = inner
    return data
