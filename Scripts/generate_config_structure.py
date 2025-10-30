import argparse
from PetriNetUtil.PNMLToDataPNML import PNMLToDataPNML


def main():
    parser = argparse.ArgumentParser(description="Generate blank config structure and wrapped PNML from a Petri net PNML file.")
    parser.add_argument("--pnml", required=True, help="Path to the original PNML file.")
    parser.add_argument("--config-out", required=True, help="Directory where the generated config file should be saved.")
    args = parser.parse_args()

    util = PNMLToDataPNML(pnml_path=args.pnml, config_dir=args.config_out)

    print(">>> Generating config structure...")
    cfg_path = util.generate_config_structure()
    print(f"Generated blank config at: {cfg_path}")

if __name__ == "__main__":
    main()
