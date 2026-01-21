from pathlib import Path
from Scripts.Util.petri_net_util import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_3/PetriNet/pnml/phase_3_repeat.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn("Scripts/Phase_2/PetriNet/pnml/phase_2_benign.pnml")
repeat_pn = deepcopy(benign_pn)

#mapping the markings
repeat_im = remap_marking(benign_im, repeat_pn)
repeat_fm = remap_marking(benign_fm, repeat_pn)

#transition
t_4624_2 = get_transition_by_id(repeat_pn, "4624_2")
t_4625_1 = PetriNet.Transition("4625_1", "4625")
t_4625_2 = PetriNet.Transition("4625_2", "4625")
t_4625_3 = PetriNet.Transition("4625_3", "4625")
t_4625_4 = PetriNet.Transition("4625_4", "4625")
t_4625_5 = PetriNet.Transition("4625_5", "4625")
t_4625_loop = PetriNet.Transition("4625_loop", "4625")

repeat_pn.transitions.update({t_4625_1, t_4625_2, t_4625_3, t_4625_4, t_4625_5, t_4625_loop})

#places
source_0 = get_place_by_id(repeat_pn, "source0")

p16 = PetriNet.Place("p16")
p17 = PetriNet.Place("p17")
p18 = PetriNet.Place("p18")
p19 = PetriNet.Place("p19")
p20 = PetriNet.Place("p20")

repeat_pn.places.update({p16, p17, p18, p19, p20})


#updating
arc_source = get_arc_by_id(repeat_pn, "source0", "4624_2")
petri_utils.remove_arc(repeat_pn, arc_source)

petri_utils.add_arc_from_to(source_0, t_4625_1, repeat_pn)
petri_utils.add_arc_from_to(t_4625_1, p16, repeat_pn)
petri_utils.add_arc_from_to(p16, t_4625_2, repeat_pn)
petri_utils.add_arc_from_to(t_4625_2, p17, repeat_pn)
petri_utils.add_arc_from_to(p17, t_4625_3, repeat_pn)
petri_utils.add_arc_from_to(t_4625_3, p18, repeat_pn)
petri_utils.add_arc_from_to(p18, t_4625_4, repeat_pn)
petri_utils.add_arc_from_to(t_4625_4, p19, repeat_pn)
petri_utils.add_arc_from_to(p19, t_4625_5, repeat_pn)
petri_utils.add_arc_from_to(t_4625_5, p20, repeat_pn)
petri_utils.add_arc_from_to(p20, t_4625_loop, repeat_pn)
petri_utils.add_arc_from_to(t_4625_loop, p20, repeat_pn)

petri_utils.add_arc_from_to(p20, t_4624_2, repeat_pn)


#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(repeat_pn, repeat_im, str(out_path), final_marking=repeat_fm)

print(f"PNML written to: {out_path}")
