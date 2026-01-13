from pathlib import Path
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.obj import PetriNet, Marking

PNML_PATH = "Scripts/Phase_2/PetriNet/pnml/phase_2_benign.pnml"

def get_benign_pn():
    pnml_path = Path(PNML_PATH).expanduser().resolve()

    if not pnml_path.is_file():
        raise FileNotFoundError(f"PNML file not found: {PNML_PATH}")

    net, initial_marking, final_marking = pnml_importer.apply(str(PNML_PATH))
    return net, initial_marking, final_marking

def get_place_by_id(net, place_id):
    for p in net.places:
        if p.name == place_id:
            return p
    raise KeyError(f"place id '{place_id}' not found in net places.")

def get_transition_by_id(net, trans_id):
    for t in net.transitions:
        if t.name == trans_id:
            return t
    raise KeyError(f"Transition id '{trans_id}' not found in net transitions.")

def remap_marking(marking, new_net):
    new_marking = Marking()
    name_to_place = {p.name: p for p in new_net.places}
    for old_place, tokens in marking.items():
        p2 = name_to_place.get(old_place.name)
        if p2 is None:
            raise KeyError(f"Place '{old_place.name}' from marking not found in new net.")
        new_marking[p2] = tokens
    return new_marking