import argparse
from PetriNetUtil.PNMLToDataPNML import generate_config_structure
from probability_mining_rogue import *

def main():
    parser = argparse.ArgumentParser(
        description="Generatexx config structure and wrapped PNML from a Petri net PNML file."
    )
    parser.add_argument("--pnml", required=True, help="Path to the original PNML file.")
    parser.add_argument("--config-out", required=True, help="Directory where the generated config file should be saved.")
    parser.add_argument("--prob-xes", required=False, help="The xes file you want to use to fill in probabilities in the config.")
    args = parser.parse_args()

    print(">>> Generating config structure...")


    cfg_path = generate_config_structure(pnml_path=args.pnml, config_dir=args.config_out)


    if args.prob_xes:
        print(">>> --prob-xes provided; mining probabilities and filling config...")
        run_probability_mining_and_fill_config(pnml_path=args.pnml, xes_path=args.prob_xes, config_json_path=cfg_path)

        print(f"Filled config: {cfg_path}")
    else:
        print(">>> No --prob-xes provided, leaving config blank.")

if __name__ == "__main__":
    main()
