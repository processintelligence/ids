import argparse
from Scripts.Simulation.pnml_to_data_pnml import generate_data_petrinet
from LogPPL.scripts.generate_uniform_traces import simulate_dpn
from Scripts.Phase_2.evtx_to_xes.evtx_util import keep_last_trace

ALLOWED_ATTACKTYPES = ("Composite", "Redflag", "Repeat", "4th")

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

    parser.add_argument(
        "--attacktype",
        default=None,
        choices=ALLOWED_ATTACKTYPES,
        help=f'Attack type to simulate. Allowed: {", ".join(ALLOWED_ATTACKTYPES)}. Leave blank for benign.'
    )


    args = parser.parse_args()

    config_path = args.config

    print(">>> Generating data PNML from config...")
    data_pnml_path = generate_data_petrinet(config_path)
    print(f"Data PNML written to: {data_pnml_path}")

    print(">>> Simulating data PNML to generate uniform traces...")
    xes_path = simulate_dpn(steps=args.steps, sample_size=args.sample_size,pnml_path=data_pnml_path,attacktype=args.attacktype)

    if args.attacktype is not None:
        keep_last_trace(xes_path)


if __name__ == "__main__":
    main()
