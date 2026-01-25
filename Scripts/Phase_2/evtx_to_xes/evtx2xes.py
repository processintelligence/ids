from Scripts.Phase_2.evtx_to_xes.evtx_util import *
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Convert one or more EVTX files to a combined CSV and then to XES."
    )

    parser.add_argument(
        "--evtx",
        nargs="+",
        required=True,
        help="One or more input .evtx file paths."
    )
    parser.add_argument(
        "--csv-out",
        required=True,
        help="Output path for the intermediate CSV."
    )
    parser.add_argument(
        "--xes-out",
        required=True,
        help="Output path for the final XES."
    )

    args = parser.parse_args()

    evtx_paths = [os.path.abspath(p) for p in args.evtx]
    csv_out = os.path.abspath(args.csv_out)
    xes_out = os.path.abspath(args.xes_out)

    missing = [p for p in evtx_paths if not os.path.exists(p)]
    if missing:
        print("ERROR: The following EVTX files were not found:", file=sys.stderr)
        for p in missing:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(2)

    os.makedirs(os.path.dirname(csv_out) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(xes_out) or ".", exist_ok=True)

    config = LogConfig()

    print(">>> EVTX -> CSV")
    evtx_to_csv(evtx_paths, csv_out)
    print(f"CSV written to: {csv_out}")

    print(">>> Detecting time windows")
    windows = get_start_and_end_from_csv(csv_out, config)
    print(f"Found {len(windows)} window(s)")

    print(">>> CSV -> XES (as well as log obtaining)")
    csv_to_xes(csv_out, xes_out, windows, config)
    print(f"XES written to: {xes_out}")

    print("Generated XES from combined EVTX files")


if __name__ == "__main__":
    main()
