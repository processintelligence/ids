from pathlib import Path
from Scripts.Phase_1.generate_phase1_petrinet_benign import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_1/pnml/phase_1_repeat.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn()
repeat_pn = deepcopy(benign_pn)

#mapping the markings
repeat_im = remap_marking(benign_im, repeat_pn)
repeat_fm = remap_marking(benign_fm, repeat_pn)

#transitions
t_4625 = PetriNet.Transition("4625", "4625")

repeat_pn.transitions.update({t_4625})

#places
p1 = get_place_by_id(repeat_pn, "p1")

#updating
petri_utils.add_arc_from_to(p1, t_4625, repeat_pn)
petri_utils.add_arc_from_to(t_4625, p1, repeat_pn)

#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(repeat_pn, repeat_im, str(out_path), final_marking=repeat_fm)

print(f"PNML written to: {out_path}")

