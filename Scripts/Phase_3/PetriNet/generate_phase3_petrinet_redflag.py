from pathlib import Path
from Scripts.Util.petri_net_util import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_3/PetriNet/pnml/phase_3_redflag.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn("Scripts/Phase_2/PetriNet/pnml/phase_2_benign_extended.pnml")
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
t_4634_2 = get_transition_by_id(redflag_pn, "4634_2")

source1 = PetriNet.Place("source1")
p20 = PetriNet.Place("p20")

redflag_pn.places.update({source1, p20})

#source1 initial marking should be 1
redflag_im[source1] = 1

#updating
petri_utils.add_arc_from_to(intplace_4663, t_4657_common, redflag_pn)
petri_utils.add_arc_from_to(t_4657_common, pre_4658, redflag_pn)

petri_utils.add_arc_from_to(source1, t_4657_common, redflag_pn)
petri_utils.add_arc_from_to(t_4657_common, p20, redflag_pn)
petri_utils.add_arc_from_to(p20, t_4634_2, redflag_pn)


#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(redflag_pn, redflag_im, str(out_path), final_marking=redflag_fm)

print(f"PNML written to: {out_path}")

