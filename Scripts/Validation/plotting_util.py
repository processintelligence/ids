import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import random

DIFF_BLACK = -999999.0
DIFF_WHITE =  999999.0

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
    ],
    "diff": [
        (0.00, "black"),
        (0.01, "navy"),
        (0.33, "deepskyblue"),
        (0.34, "green"),
        (0.66, "lime"),
        (0.67, "orangered"),
        (0.99, "darkred"),
        (1.00, "white"),
    ],
}

def get_colormap(scheme_name: str) -> LinearSegmentedColormap:
    if scheme_name not in COLOR_SCHEMES:
        raise ValueError(f"Unknown color scheme '{scheme_name}'. "
                         f"Available: {list(COLOR_SCHEMES.keys())}")
    return LinearSegmentedColormap.from_list(
        f"dfg_{scheme_name}",
        COLOR_SCHEMES[scheme_name]
    )

def nested_map_to_matrix(nested_map):
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
    color_scheme="4-band",
    interpolation="nearest",
    figsize_scale=0.3
):
    mat, labels, idx = nested_map_to_matrix(nested_map)
    n = len(labels)

    # Normalize special diff values
    if color_scheme == "diff":
        m = mat.copy()
        mask_black = (m == DIFF_BLACK)
        mask_white = (m == DIFF_WHITE)
        normal = m[~(mask_black | mask_white)]
        if normal.size > 0:
            lo, hi = normal.min(), normal.max()
        else:
            lo, hi = 0, 1
        m = (m - lo) / (hi - lo + 1e-12)
        m[mask_black] = 0.0
        m[mask_white] = 1.0
        mat = m

    cmap = get_colormap(color_scheme)

    fig, ax = plt.subplots(figsize=(1.0 + figsize_scale * n,
                                    1.0 + figsize_scale * n))

    im = ax.imshow(mat, cmap=cmap, interpolation=interpolation)

    ax.set_xticks(range(n), labels=labels, rotation=90, fontsize=8)
    ax.set_yticks(range(n), labels=labels, fontsize=8)
    ax.set_xlabel("follows → (destination)")
    ax.set_ylabel("source")
    ax.set_title(title)

    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle="-", linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("count", rotation=270, labelpad=12)

    plt.tight_layout()
    plt.show()


def diff_maps(mapA, mapB):
    diff = {}
    for src in mapA:
        diff[src] = {}
        for dst in mapA[src]:
            a = mapA[src].get(dst, 0.0)
            b = mapB[src].get(dst, 0.0)
            diff[src][dst] = a - b
    return diff


def diff_maps_bw(mapA, mapB):
    diff = {}
    for src in mapA:
        diff[src] = {}
        for dst in mapA[src]:
            a = mapA[src].get(dst, 0.0)
            b = mapB[src].get(dst, 0.0)

            if a == 0 and b == 0:
                diff[src][dst] = 0.0
            elif a == 0 and b > 0:
                diff[src][dst] = DIFF_WHITE
            elif a > 0 and b == 0 and a > 0.1:
                diff[src][dst] = DIFF_BLACK
            else:
                diff[src][dst] = a - b

    return diff

def generate_random_directly_follows_data(n=20, min_val=0, max_val=20, seed=42):
    random.seed(seed)
    labels = [f"Act_{i:02d}" for i in range(1, n + 1)]
    data = {}
    for src in labels:
        inner = {}
        for dst in labels:
            inner[dst] = 0 if src == dst else random.randint(min_val, max_val)
        data[src] = inner
    return data
