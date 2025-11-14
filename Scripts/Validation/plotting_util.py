import matplotlib.pyplot as plt
import numpy as np
import random

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize

def validate_maps(nested_map1, nested_map2):
    keys1, keys2 = set(nested_map1.keys()), set(nested_map2.keys())
    all_keys = keys1.union(keys2)

    for key in all_keys:
        if key not in nested_map1:
            nested_map1[key] = {}
        if key not in nested_map2:
            nested_map2[key] = {}

    """  all_inner_keys = set()
    for outer_key in all_keys:
        all_inner_keys.update(nested_map1[outer_key].keys())
        all_inner_keys.update(nested_map2[outer_key].keys()) """

    for outer_key in all_keys:
        for inner_key in all_keys:
            if inner_key not in nested_map1[outer_key]:
                nested_map1[outer_key][inner_key] = 0
            if inner_key not in nested_map2[outer_key]:
                nested_map2[outer_key][inner_key] = 0

    return nested_map1, nested_map2


def plot_directly_follows_heatmap_3_col(nested_map, title="Directly-Follows Heatmap"):
    labels = sorted(nested_map.keys())
    idx = {lab: i for i, lab in enumerate(labels)}
    n = len(labels)

    mat = np.zeros((n, n), dtype=float)
    for src, inner in nested_map.items():
        i = idx[src]
        for dst, count in inner.items():
            if dst in idx:
                j = idx[dst]
                mat[i, j] = float(count or 0)

    colors = [
        (0.00, "navy"),
        (0.33, "deepskyblue"),
        (0.34, "green"),
        (0.66, "lime"),
        (0.67, "orangered"),
        (1.00, "darkred")
    ]
    cmap = LinearSegmentedColormap.from_list("custom_heat", colors)

    fig, ax = plt.subplots(figsize=(1.0 + 0.3 * n, 1.0 + 0.3 * n))
    im = ax.imshow(mat, cmap=cmap, interpolation="bilinear")

    ax.set_xticks(range(n), labels=labels, rotation=90, fontsize=8)
    ax.set_yticks(range(n), labels=labels, fontsize=8)
    ax.set_xlabel("follows → (destination)")
    ax.set_ylabel("source")
    ax.set_title(title)

    if n <= 15:
        for i in range(n):
            for j in range(n):
                ax.text(j, i, f"{mat[i, j]:.0f}", ha="center", va="center",
                        fontsize=7, color="black")

    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("count", rotation=270, labelpad=12)

    plt.tight_layout()
    plt.show()

def plot_directly_follows_heatmap_4_col(nested_map, title="Directly-Follows Heatmap"):
    labels = sorted(nested_map.keys())
    idx = {lab: i for i, lab in enumerate(labels)}
    n = len(labels)

    mat = np.zeros((n, n), dtype=float)
    for src, inner in nested_map.items():
        i = idx[src]
        for dst, count in inner.items():
            if dst in idx:
                j = idx[dst]
                mat[i, j] = float(count or 0)

    colors = [
        (0.00, "navy"),
        (0.25, "deepskyblue"),
        (0.26, "green"),
        (0.50, "lime"),
        (0.51, "yellow"),
        (0.75, "gold"),
        (0.76, "orangered"),
        (1.00, "darkred")
    ]
    cmap = LinearSegmentedColormap.from_list("custom_heat", colors)

    fig, ax = plt.subplots(figsize=(1.0 + 0.3 * n, 1.0 + 0.3 * n))
    im = ax.imshow(mat, cmap=cmap, interpolation="bilinear")

    ax.set_xticks(range(n), labels=labels, rotation=90, fontsize=8)
    ax.set_yticks(range(n), labels=labels, fontsize=8)
    ax.set_xlabel("follows → (destination)")
    ax.set_ylabel("source")
    ax.set_title(title)

    if n <= 15:
        for i in range(n):
            for j in range(n):
                ax.text(j, i, f"{mat[i, j]:.0f}", ha="center", va="center",
                        fontsize=7, color="black")

    cbar = plt.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("count", rotation=270, labelpad=12)

    plt.tight_layout()
    plt.show()

def generate_random_directly_follows_data(n=30, min_val=0, max_val=20, seed=42):
    random.seed(seed)
    labels = [f"Act_{i:02d}" for i in range(1, n + 1)]
    data = {}
    for src in labels:
        inner = {}
        for dst in labels:
            inner[dst] = 0 if src == dst else random.randint(min_val, max_val)
        data[src] = inner
    return data


def diff_maps(mapA, mapB):
    diff = {}
    for src in mapA:
        diff[src] = {}
        for dst in mapA[src]:
            valA = mapA[src].get(dst, 0.0)
            valB = mapB[src].get(dst, 0.0)
            diff[src][dst] = valA - valB
    return diff

