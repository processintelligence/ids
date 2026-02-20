import argparse
from Scripts.Validation.evaluation_metrics import compute_fitness, compute_precision

def main():
    parser = argparse.ArgumentParser(
        description="Compute fitness and precision of a Petri net against an XES log."
    )
    parser.add_argument("pnml_path", help="Path to the PNML file")
    parser.add_argument("xes_path", help="Path to the XES log file")

    args = parser.parse_args()

    fitness = compute_fitness(args.pnml_path, args.xes_path)
    print("Fitness score:", fitness)

    precision = compute_precision(args.pnml_path, args.xes_path)
    print("Precision score:", precision)

if __name__ == "__main__":
    main()