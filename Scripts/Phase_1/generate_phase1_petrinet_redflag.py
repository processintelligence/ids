from pathlib import Path
from Scripts.Util.petri_net_util import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_1/pnml/phase_1_redflag.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn("Scripts/Phase_1/pnml/phase_1_benign.pnml")
redflag_pn = deepcopy(benign_pn)

#mapping the markings
redflag_im = remap_marking(benign_im, redflag_pn)
redflag_fm = remap_marking(benign_fm, redflag_pn)

#transitions
t_4656 = PetriNet.Transition("4656", "4656")
t_4657_common = PetriNet.Transition("4657_common", "4657_common")
t_4658 = PetriNet.Transition("4658", "4658")
t_4663 = PetriNet.Transition("4663", "4663")

redflag_pn.transitions.update({t_4656, t_4657_common, t_4658, t_4663})

#places
p19 = PetriNet.Place("p19")
p20 = PetriNet.Place("p20")
p21 = PetriNet.Place("p21")

redflag_pn.places.update({p19, p20, p21})

p17 = get_place_by_id(redflag_pn, "p17")
p6 = get_place_by_id(redflag_pn, "p6")

#updating
petri_utils.add_arc_from_to(p17, t_4656, redflag_pn)
petri_utils.add_arc_from_to(t_4656, p19, redflag_pn)
petri_utils.add_arc_from_to(p19, t_4663, redflag_pn)
petri_utils.add_arc_from_to(t_4663, p20, redflag_pn)
petri_utils.add_arc_from_to(p20, t_4657_common, redflag_pn)
petri_utils.add_arc_from_to(t_4657_common, p21, redflag_pn)
petri_utils.add_arc_from_to(p21, t_4658, redflag_pn)
petri_utils.add_arc_from_to(t_4658, p6, redflag_pn)

#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(redflag_pn, redflag_im, str(out_path), final_marking=redflag_fm)

print(f"PNML written to: {out_path}")

