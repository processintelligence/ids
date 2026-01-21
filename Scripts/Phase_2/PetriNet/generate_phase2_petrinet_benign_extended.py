from pathlib import Path
from Scripts.Util.petri_net_util import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_2/PetriNet/pnml/phase_2_benign_extended.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn("Scripts/Phase_2/PetriNet/pnml/phase_2_benign.pnml")
benign_ext_pn = deepcopy(benign_pn)

#mapping the markings
benign_ext_im = remap_marking(benign_im, benign_ext_pn)
benign_ext_fm = remap_marking(benign_fm, benign_ext_pn)

#transitions
t_4624_2 = get_transition_by_id(benign_ext_pn, "4624_2")
t_4625_1 = PetriNet.Transition("4625_1", "4625")
t_4625_2 = PetriNet.Transition("4625_2", "4625")
t_4625_3 = PetriNet.Transition("4625_3", "4625")
t_4625_4 = PetriNet.Transition("4625_4", "4625")

tau_17 = PetriNet.Transition("tau_17", None)
tau_18 = PetriNet.Transition("tau_18", None)
tau_19 = PetriNet.Transition("tau_19", None)
tau_20 = PetriNet.Transition("tau_20", None)

benign_ext_pn.transitions.update({t_4625_1, t_4625_2, t_4625_3, t_4625_4, tau_17, tau_18, tau_19, tau_20})

#places
source_0 = get_place_by_id(benign_ext_pn, "source0")

p16 = PetriNet.Place("p16")
p17 = PetriNet.Place("p17")
p18 = PetriNet.Place("p18")
p19 = PetriNet.Place("p19")


benign_ext_pn.places.update({p16, p17, p18, p19})

#updating
arc_source = get_arc_by_id(benign_ext_pn, "source0", "4624_2")
petri_utils.remove_arc(benign_ext_pn, arc_source)

petri_utils.add_arc_from_to(source_0, tau_17, benign_ext_pn)
petri_utils.add_arc_from_to(tau_17, p16, benign_ext_pn)
petri_utils.add_arc_from_to(p16, t_4624_2, benign_ext_pn)

petri_utils.add_arc_from_to(source_0, t_4625_1, benign_ext_pn)
petri_utils.add_arc_from_to(t_4625_1, p17, benign_ext_pn)
petri_utils.add_arc_from_to(p17, tau_18, benign_ext_pn)
petri_utils.add_arc_from_to(tau_18, p16, benign_ext_pn)
petri_utils.add_arc_from_to(p17, t_4625_2, benign_ext_pn)
petri_utils.add_arc_from_to(t_4625_2, p18, benign_ext_pn)
petri_utils.add_arc_from_to(p18, tau_19, benign_ext_pn)
petri_utils.add_arc_from_to(tau_19, p16, benign_ext_pn)
petri_utils.add_arc_from_to(p18, t_4625_3, benign_ext_pn)
petri_utils.add_arc_from_to(t_4625_3, p19, benign_ext_pn)
petri_utils.add_arc_from_to(p19, tau_20, benign_ext_pn)
petri_utils.add_arc_from_to(tau_20, p16, benign_ext_pn)
petri_utils.add_arc_from_to(p19, t_4625_4, benign_ext_pn)
petri_utils.add_arc_from_to(t_4625_4, p16, benign_ext_pn)


#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(benign_ext_pn, benign_ext_im, str(out_path), final_marking=benign_ext_fm)

print(f"PNML written to: {out_path}")

