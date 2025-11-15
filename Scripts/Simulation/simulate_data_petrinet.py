import argparse
from PetriNetUtil.PNMLToDataPNML import generate_data_petrinet
from LogPPL.scripts.generate_uniform_traces import simulate_dpn

def main(): 
    parser = argparse.ArgumentParser(
        description="Generate data PNML by injecting variables, guards, write variables, and simulate uniform traces."
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the config JSON file created by generate_config_structure."
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=10,
        help="Number of simulation steps (default: 10)."
    )

    parser.add_argument(
        "--sample-size",
        type=int,
        default=100,
        help="Number of traces to sample during simulation (default: 100)."
    )

    args = parser.parse_args()

    config_path = args.config

    print(">>> Generating data PNML from config...")
    data_pnml_path = generate_data_petrinet(config_path)
    print(f"Data PNML written to: {data_pnml_path}")

    print(">>> Simulating data PNML to generate uniform traces...")
    simulate_dpn(
        steps=args.steps,
        sample_size=args.sample_size,
        pnml_path=data_pnml_path
    )

if __name__ == "__main__":
    main()
