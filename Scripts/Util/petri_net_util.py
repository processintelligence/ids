from pathlib import Path
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.obj import PetriNet, Marking

def get_benign_pn(pnml_path):
    pnml_path = Path(pnml_path).expanduser().resolve()

    if not pnml_path.is_file():
        raise FileNotFoundError(f"PNML file not found: {pnml_path}")

    net, initial_marking, final_marking = pnml_importer.apply(str(pnml_path))
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

def get_node_by_id(net, node_id):
    for p in net.places:
        if p.name == node_id:
            return p
    for t in net.transitions:
        if t.name == node_id:
            return t
    raise KeyError(f"Node id '{node_id}' not found in net (places or transitions).")

def get_arc_by_id(net, source_id, target_id):
    src = get_node_by_id(net, source_id)
    tgt = get_node_by_id(net, target_id)

    for a in net.arcs:
        if a.source == src and a.target == tgt:
            return a

    raise KeyError(f"Arc '{source_id}' -> '{target_id}' not found in net.")

def remap_marking(marking, new_net):
    new_marking = Marking()
    name_to_place = {p.name: p for p in new_net.places}
    for old_place, tokens in marking.items():
        p2 = name_to_place.get(old_place.name)
        if p2 is None:
            raise KeyError(f"Place '{old_place.name}' from marking not found in new net.")
        new_marking[p2] = tokens
    return new_marking