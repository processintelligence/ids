import json
import os
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
PNML_NS = "http://www.pnml.org/version-2009/grammar/pnml"
NS = {"pnml": PNML_NS}
ET.register_namespace("", PNML_NS)


class IPetriNetUtil(ABC):
    @abstractmethod
    def get_petrinet(self, pnml):
        pass
    @abstractmethod
    def create_blanc_config(self, petrinet, output_path):
        pass
    @abstractmethod
    def get_data_pnml(self, petrinet, config):
        pass


class PetriNetUtil(IPetriNetUtil):
    def __init__(self):
        pass

    def get_petrinet(self, pnml_path):
        net, initial_marking, final_marking = pnml_importer.apply(pnml_path)
        return net, initial_marking, final_marking

    def create_blanc_config(self, petrinet, output_path):
        config = {
            "name": "",
            "behavior": "",
            "transitions": {t.name: "" for t in petrinet.transitions}
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return config

    def create_pnml(self, net, im, fm, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        pnml_exporter.apply(net, im, output_path, final_marking=fm)

    def add_guards(self, pnml_path, config):
        # Load config if a path was provided
        if isinstance(config, str) and os.path.exists(config):
            with open(config, "r", encoding="utf-8") as f:
                config = json.load(f)

        guards = (config or {}).get("transitions", {})
        if not isinstance(guards, dict):
            raise ValueError("Config must contain a 'transitions' object.")

        # Parse PNML
        tree = ET.parse(pnml_path)
        root = tree.getroot()

        # For each transition in config, set guard attribute
        for t_id, guard in guards.items():
            xpath = f".//pnml:transition[@id='{t_id}']"
            matches = root.findall(xpath, NS)
            if not matches:
                print(f"Transition '{t_id}' not found in PNML; skipping.")
                continue
            for t_el in matches:
                t_el.set("guard", "" if guard is None else str(guard))

        # Write PNML back
        tree.write(pnml_path, encoding="utf-8", xml_declaration=True)
        print(f"Guards written to: {pnml_path}")

    def get_data_pnml(self, net, im, fm, config, output_path):
        """Export PNML, then inject guards based on config."""
        self.create_pnml(net, im, fm, output_path)
        self.add_guards(output_path, config)
        # TODO: add variables at bottom if needed later
        return output_path

# -----------------------------------
if __name__ == "__main__":
    # Input and output paths
    pnml_file = "PNMLFiles/simple_petrinet.pnml"
    config_path = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/Configs/config1.json"
    output_pnml = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/PNMLFiles/output_with_guards.pnml"

    # Initialize the utility
    util = PetriNetUtil()

    # --- Load Petri net ---
    net, im, fm = util.get_petrinet(pnml_file)
    print("Petri net loaded successfully!")
    print(f"Net name: {net.name}")
    print("Places:", [p.name for p in net.places])
    print("Transitions:", [t.name for t in net.transitions])
    print("Initial marking:", {p.name: t for p, t in im.items()})

    # --- Create blank config ---
    config = util.create_blanc_config(net, config_path)
    print("\nGenerated blank config:")
    print(json.dumps(config, indent=4))

    # --- Add guards and export PNML with data ---
    new_pnml = util.get_data_pnml(net, im, fm, config_path, output_pnml)
    print(f"\nData PNML written to: {new_pnml}")
