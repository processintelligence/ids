import matplotlib.pyplot as plt
import numpy as np
import random


def plot_directly_follows_heatmap(nested_map, title="Directly-Follows Heatmap"):
    labels = sorted(nested_map.keys())
    idx = {lab: i for i, lab in enumerate(labels)}
    n = len(labels)

    mat = np.zeros((n, n), dtype=int)
    for src, inner in nested_map.items():
        i = idx[src]
        for dst, count in inner.items():
            if dst in idx:
                j = idx[dst]
                mat[i, j] = int(count or 0)

    fig, ax = plt.subplots(figsize=(1.0 + 0.3 * n, 1.0 + 0.3 * n))

    im = ax.imshow(
        mat,
        cmap="YlOrRd",
        interpolation="bilinear"
    )

    ax.set_xticks(range(n), labels=labels, rotation=90, fontsize=8)
    ax.set_yticks(range(n), labels=labels, fontsize=8)
    ax.set_xlabel("follows → (destination)")
    ax.set_ylabel("source")
    ax.set_title(title)

    if n <= 15:
        for i in range(n):
            for j in range(n):
                ax.text(j, i, str(mat[i, j]), ha="center", va="center", fontsize=7, color="black")

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