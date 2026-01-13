from pathlib import Path
from Scripts.Phase_2.PetriNet.generate_phase2_petrinet_benign import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_2/PetriNet/pnml/phase_2_4th.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn()
fourth_pn = deepcopy(benign_pn)

#mapping the markings
fourth_im = remap_marking(benign_im, fourth_pn)
fourth_fm = remap_marking(benign_fm, fourth_pn)

#transition
t_4657_lsa = fourth_pn.Transition("4657_lsa", "4657_lsa")
t_4688_passworddll = fourth_pn.Transition("4688_passworddll", "4688_passworddll")


fourth_pn.transitions.update({t_4657_lsa, t_4688_passworddll})

#places
intplace_4663 = get_place_by_id(fourth_pn, "intplace_4663")
pre_4658 = get_place_by_id(fourth_pn, "pre_4658")

pre_4688_cmd = get_place_by_id(fourth_pn, "pre_4688_cmd")
intplace_4688_cmd = get_place_by_id(fourth_pn, "intplace_4688_cmd")

#updating
petri_utils.add_arc_from_to(intplace_4663, t_4657_lsa, fourth_pn)
petri_utils.add_arc_from_to(t_4657_lsa, pre_4658, fourth_pn)

petri_utils.add_arc_from_to(pre_4688_cmd, t_4688_passworddll, fourth_pn)
petri_utils.add_arc_from_to(t_4688_passworddll, intplace_4688_cmd, fourth_pn)

#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(fourth_pn, fourth_im, str(out_path), final_marking=fourth_fm)

print(f"PNML written to: {out_path}")
