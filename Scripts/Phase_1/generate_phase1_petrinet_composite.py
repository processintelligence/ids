from pathlib import Path
from Scripts.Util.petri_net_util import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_1/pnml/phase_1_composite.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn("Scripts/Phase_1/pnml/phase_1_benign.pnml")
composite_pn = deepcopy(benign_pn)

#mapping the markings
composite_im = remap_marking(benign_im, composite_pn)
composite_fm = remap_marking(benign_fm, composite_pn)

#transitions
t_4656 = PetriNet.Transition("4656", "4656")
t_4657 = PetriNet.Transition("4657", "4657")
t_4658 = PetriNet.Transition("4658", "4658")
t_4663 = PetriNet.Transition("4663", "4663")
t_4648 = PetriNet.Transition("4648", "4648")
tau_11 = PetriNet.Transition("tau_11", None)

t_4624_4 = get_transition_by_id(composite_pn, "4624_4")

composite_pn.transitions.update({t_4656, t_4657, t_4658, t_4663, tau_11, t_4648})

#places
p19 = PetriNet.Place("p19")
p20 = PetriNet.Place("p20")
p21 = PetriNet.Place("p21")
p22 = PetriNet.Place("p22")

composite_pn.places.update({p19, p20, p21, p22})

p17 = get_place_by_id(composite_pn, "p17")
p6 = get_place_by_id(composite_pn, "p6")
p11 = get_place_by_id(composite_pn, "p11")


#arcs
arc_p11_4624_4 = get_arc_by_id(composite_pn, "p11", "4624_4")
petri_utils.remove_arc(composite_pn, arc_p11_4624_4)

#updating
petri_utils.add_arc_from_to(p17, t_4656, composite_pn)
petri_utils.add_arc_from_to(t_4656, p19, composite_pn)
petri_utils.add_arc_from_to(p19, t_4663, composite_pn)
petri_utils.add_arc_from_to(t_4663, p20, composite_pn)
petri_utils.add_arc_from_to(p20, tau_11, composite_pn)
petri_utils.add_arc_from_to(p20, t_4657, composite_pn)
petri_utils.add_arc_from_to(tau_11, p21, composite_pn)
petri_utils.add_arc_from_to(t_4657, p21, composite_pn)
petri_utils.add_arc_from_to(p21, t_4658, composite_pn)
petri_utils.add_arc_from_to(t_4658, p6, composite_pn)

petri_utils.add_arc_from_to(p11, t_4648, composite_pn)
petri_utils.add_arc_from_to(t_4648, p22, composite_pn)
petri_utils.add_arc_from_to(p22, t_4624_4, composite_pn)





#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(composite_pn, composite_im, str(out_path), final_marking=composite_fm)

print(f"PNML written to: {out_path}")

