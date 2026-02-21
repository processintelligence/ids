from .evaluation_metrics import compute_alignment_fitness
import os
import argparse
from typing import Dict, Optional

def clean_pnml_name(path):
    """Convert a PNML filepath into a nicer display name."""
    name = os.path.basename(path)
    # Strip extension
    if name.lower().endswith(".pnml"):
        name = name[:-5]
    # Strip known prefixes/suffixes
    for prefix in ("phase_1_", "phase_2_", "phase_3_"):
        if name.startswith(prefix):
            name = name[len(prefix):]
    name = name.replace("_extended", "")
    return name


def clean_xes_name(path):
    """Convert an XES filepath into a nicer display name."""
    name = os.path.basename(path)
    if name.lower().endswith(".xes"):
        name = name[:-4]
    return name


def print_conformance_table(conformance_table, xes_paths):
    print("Conformance Table (Fitness)")
    print("=" * 50)

    header = "PNML/XES\t" + "\t".join([clean_xes_name(x) for x in xes_paths])
    print(header)

    for pnml_name in conformance_table:
        row = pnml_name + "\t"
        for xes_name in conformance_table[pnml_name]:
            value = conformance_table[pnml_name][xes_name]
            row += f"{value:.3f}\t" if value is not None else "N/A\t"
        print(row)


def validate_paths(paths, kind):
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        msg = "\n".join(f"  - {p}" for p in missing)
        raise FileNotFoundError(f"Missing {kind} file(s):\n{msg}")


def build_conformance_table(
    pnml_paths,
    xes_paths,
    clean_names: bool = True
):
    # Dict: {pnml_display_name: {xes_display_name: fitness}}
    table: Dict[str, Dict[str, Optional[float]]] = {}

    for pnml_path in pnml_paths:
        pnml_display = clean_pnml_name(pnml_path) if clean_names else os.path.basename(pnml_path)
        table[pnml_display] = {}

        for xes_path in xes_paths:
            xes_display = clean_xes_name(xes_path) if clean_names else os.path.basename(xes_path)

            try:
                fitness = compute_alignment_fitness(pnml_path, xes_path)
                table[pnml_display][xes_display] = fitness
            except Exception as e:
                print(f"Error computing fitness for {pnml_display} and {xes_display}: {e}")
                table[pnml_display][xes_display] = None

    return table


def main():
    parser = argparse.ArgumentParser(
        description="Compute a conformance (fitness) table for PNML and XES combinations."
    )

    parser.add_argument(
        "--pnml",
        nargs="+",
        required=True,
        help="List of PNML files (space-separated)."
    )

    parser.add_argument(
        "--xes",
        nargs="+",
        required=True,
        help="List of XES files (space-separated)."
    )

    parser.add_argument(
        "--no-clean-names",
        action="store_true",
        help="Do not normalize display names; show full basenames."
    )

    args = parser.parse_args()

    # Validate input files exist
    validate_paths(args.pnml, "PNML")
    validate_paths(args.xes, "XES")

    conformance_table = build_conformance_table(
        pnml_paths=args.pnml,
        xes_paths=args.xes,
        clean_names=not args.no_clean_names
    )

    print_conformance_table(conformance_table, args.xes)


if __name__ == "__main__":
    main()