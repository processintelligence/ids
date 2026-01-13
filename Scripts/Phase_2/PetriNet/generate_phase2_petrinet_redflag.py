from pathlib import Path
from Scripts.Phase_2.PetriNet.generate_phase2_petrinet_benign import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_2/PetriNet/pnml/phase_2_redflag.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn()
redflag_pn = deepcopy(benign_pn)

#mapping the markings
redflag_im = remap_marking(benign_im, redflag_pn)
redflag_fm = remap_marking(benign_fm, redflag_pn)

#transitions
t_4657_common = PetriNet.Transition("4657_common", "4657_common")
redflag_pn.transitions.add(t_4657_common)

#places
intplace_4663 = get_place_by_id(redflag_pn, "intplace_4663")
pre_4658 = get_place_by_id(redflag_pn, "pre_4658")

#updating
petri_utils.add_arc_from_to(intplace_4663, t_4657_common, redflag_pn)
petri_utils.add_arc_from_to(t_4657_common, pre_4658, redflag_pn)

#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(redflag_pn, redflag_im, str(out_path), final_marking=redflag_fm)

print(f"PNML written to: {out_path}")

