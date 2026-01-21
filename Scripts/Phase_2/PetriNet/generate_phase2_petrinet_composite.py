from pathlib import Path
from Scripts.Util.petri_net_util import *
from copy import deepcopy
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter

OUTPUT_PNML_PATH = "Scripts/Phase_2/PetriNet/pnml/phase_2_composite.pnml"

#petri nets
benign_pn, benign_im, benign_fm = get_benign_pn("Scripts/Phase_2/PetriNet/pnml/phase_2_benign_extended.pnml")
composite_pn = deepcopy(benign_pn)

#mapping the markings
composite_im = remap_marking(benign_im, composite_pn)
composite_fm = remap_marking(benign_fm, composite_pn)

#transition
t_4657 = composite_pn.Transition("4657", "4657")
t_4624_4 = composite_pn.Transition("4624_4", "4624_4")
t_4672_4 = composite_pn.Transition("4672_4", "4672_4")
t_4634_4 = composite_pn.Transition("4634_4", "4634_4")
t_4648 = composite_pn.Transition("4648", "4648")

composite_pn.transitions.update({t_4657, t_4624_4, t_4672_4, t_4634_4, t_4648})

#places
p20 = PetriNet.Place("p20")
p21 = PetriNet.Place("p21")
p22 = PetriNet.Place("p22")

composite_pn.places.update({p20, p21, p22})

intplace_4663 = get_place_by_id(composite_pn, "intplace_4663")
pre_4658 = get_place_by_id(composite_pn, "pre_4658")
pre_4624_3 = get_place_by_id(composite_pn, "pre_4624_3")
intplace_4634_3 = get_place_by_id(composite_pn, "intplace_4634_3")

#updating
petri_utils.add_arc_from_to(intplace_4663, t_4657, composite_pn)
petri_utils.add_arc_from_to(t_4657, pre_4658, composite_pn)

petri_utils.add_arc_from_to(pre_4624_3, t_4648, composite_pn)
petri_utils.add_arc_from_to(t_4648, p20, composite_pn)
petri_utils.add_arc_from_to(p20, t_4624_4, composite_pn)
petri_utils.add_arc_from_to(t_4624_4, p21, composite_pn)
petri_utils.add_arc_from_to(p21, t_4672_4, composite_pn)
petri_utils.add_arc_from_to(t_4672_4, p22, composite_pn)
petri_utils.add_arc_from_to(p22, t_4634_4, composite_pn)
petri_utils.add_arc_from_to(t_4634_4, intplace_4634_3, composite_pn)


#export to pnml
out_path = Path(OUTPUT_PNML_PATH).expanduser().resolve()
out_path.parent.mkdir(parents=True, exist_ok=True)

pnml_exporter.apply(composite_pn, composite_im, str(out_path), final_marking=composite_fm)

print(f"PNML written to: {out_path}")
