import argparse
from PetriNetUtil.PNMLToDataPNML import PNMLToDataPNML


def main():
    parser = argparse.ArgumentParser(description="Generate data PNML by injecting variables, guards, and write variables using a config JSON.")
    parser.add_argument("--pnml", required=True, help="Path to the original PNML file (same one used to create the config).")
    parser.add_argument("--config-out", required=True, help="Directory where configs are stored (same as before).")
    args = parser.parse_args()

    util = PNMLToDataPNML(pnml_path=args.pnml, config_dir=args.config_out)

    print(">>> Generating data PNML from config...")
    data_pnml_path = util.generate_data_petrinet()
    print(f"Data PNML written to: {data_pnml_path}")

if __name__ == "__main__":
    main()
