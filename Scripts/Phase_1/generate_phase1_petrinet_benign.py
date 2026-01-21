from pathlib import Path
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.visualization.petri_net import visualizer as pn_visualizer
import os

pnml_name = "phase_1_benign.pnml"

net = PetriNet("phase_1_benign")

# Places
p1 = PetriNet.Place("p1")
p2 = PetriNet.Place("p2")
p3 = PetriNet.Place("p3")
p4 = PetriNet.Place("p4")
p5 = PetriNet.Place("p5")
p6 = PetriNet.Place("p6")
p7 = PetriNet.Place("p7")
p8 = PetriNet.Place("p8")
p9 = PetriNet.Place("p9")
p10 = PetriNet.Place("p10")
p11 = PetriNet.Place("p11")
p12 = PetriNet.Place("p12")
p13 = PetriNet.Place("p13")
p14 = PetriNet.Place("p14")
p15 = PetriNet.Place("p15")
p16 = PetriNet.Place("p16")
p17 = PetriNet.Place("p17")
p18 = PetriNet.Place("p18")
pSource = PetriNet.Place("Source")
pSink = PetriNet.Place("Sink")

net.places.update({
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13,
    p14, p15, p16, p17, p18, pSource, pSink
})

# Transitions
t_4608 = PetriNet.Transition("4608", "4608")
t_4624_3 = PetriNet.Transition("4624_3", "4624_3")
t_4634_3 = PetriNet.Transition("4634_3", "4634_3")
t_1100 = PetriNet.Transition("1100", "1100")
t_4609 = PetriNet.Transition("4609", "4609")
t_4624_9 = PetriNet.Transition("4624_9", "4624_9")
t_4624_8 = PetriNet.Transition("4624_8", "4624_8")
t_4624_2 = PetriNet.Transition("4624_2", "4624_2")
t_4624_7 = PetriNet.Transition("4624_7", "4624_7")
t_4634_2_7_8_9 = PetriNet.Transition("4634_2_7_8_9", "4634_2_7_8_9")

t_4800 = PetriNet.Transition("4800", "4800")
t_4801 = PetriNet.Transition("4801", "4801")

t_4624_4 = PetriNet.Transition("4624_4", "4624_4")
t_4634_4 = PetriNet.Transition("4634_4", "4634_4")
t_4634_5 = PetriNet.Transition("4634_5", "4634_5")
t_4624_5 = PetriNet.Transition("4624_5", "4624_5")

t_4672 = PetriNet.Transition("4672", "4672")
t_4672_3 = PetriNet.Transition("4672_3", "4672_3")
t_4672_4 = PetriNet.Transition("4672_4", "4672_4")
t_4672_5 = PetriNet.Transition("4672_5", "4672_5")

t_4688_cmd = PetriNet.Transition("4688_cmd", "4688_cmd")
t_4688_conhost = PetriNet.Transition("4688_conhost", "4688_conhost")
t_4688_priv = PetriNet.Transition("4688_priv", "4688_priv")
t_4688_unpriv = PetriNet.Transition("4688_unpriv", "4688_unpriv")

tau_1 = PetriNet.Transition("tau_1", None)
tau_2 = PetriNet.Transition("tau_2", None)
tau_3 = PetriNet.Transition("tau_3", None)
tau_4 = PetriNet.Transition("tau_4", None)
tau_5 = PetriNet.Transition("tau_5", None)
tau_6 = PetriNet.Transition("tau_6", None)
tau_7 = PetriNet.Transition("tau_7", None)
tau_8 = PetriNet.Transition("tau_8", None)
tau_9 = PetriNet.Transition("tau_9", None)
tau_10 = PetriNet.Transition("tau_10", None)

net.transitions.update({
    t_4608, t_4624_3, t_4634_3, t_1100, t_4609,
    t_4624_9, t_4624_8, t_4624_2, t_4624_7, t_4634_2_7_8_9,
    t_4800, t_4801,
    t_4624_4, t_4634_4, t_4634_5, t_4624_5,
    t_4672, t_4672_3, t_4672_4, t_4672_5,
    t_4688_cmd, t_4688_conhost, t_4688_priv, t_4688_unpriv,
    tau_1, tau_2, tau_3, tau_4, tau_5, tau_6, tau_7, tau_8, tau_9, tau_10
})


# place -> transition
petri_utils.add_arc_from_to(pSource, t_4608, net)


petri_utils.add_arc_from_to(p1, t_4624_9, net)
petri_utils.add_arc_from_to(p1, t_4624_8, net)
petri_utils.add_arc_from_to(p1, t_4624_2, net)
petri_utils.add_arc_from_to(p1, t_4624_7, net)
petri_utils.add_arc_from_to(p1, tau_6, net)

petri_utils.add_arc_from_to(p2, t_4624_3, net)

petri_utils.add_arc_from_to(p3, t_4672_3, net)
petri_utils.add_arc_from_to(p3, tau_9, net)

petri_utils.add_arc_from_to(p4, t_4634_3, net)

petri_utils.add_arc_from_to(p5, tau_8, net)

petri_utils.add_arc_from_to(p6, tau_4, net)
petri_utils.add_arc_from_to(p6, t_4634_2_7_8_9, net)

petri_utils.add_arc_from_to(p7, tau_1, net)
petri_utils.add_arc_from_to(p7, t_4800, net)
petri_utils.add_arc_from_to(p7, tau_2, net)

petri_utils.add_arc_from_to(p8, t_4801, net)

petri_utils.add_arc_from_to(p9, t_4688_unpriv, net)

petri_utils.add_arc_from_to(p10, t_4672, net)

petri_utils.add_arc_from_to(p11, t_4624_5, net)
petri_utils.add_arc_from_to(p11, t_4624_4, net)
petri_utils.add_arc_from_to(p11, tau_3, net)
petri_utils.add_arc_from_to(p11, tau_7, net)
petri_utils.add_arc_from_to(p11, t_4688_cmd, net)


petri_utils.add_arc_from_to(p12, t_4672_4, net)
petri_utils.add_arc_from_to(p12, tau_10, net)

petri_utils.add_arc_from_to(p13, t_4634_4, net)

petri_utils.add_arc_from_to(p14, t_4672_5, net)

petri_utils.add_arc_from_to(p15, t_4634_5, net)

petri_utils.add_arc_from_to(p16, t_4688_conhost, net)

petri_utils.add_arc_from_to(p17, t_4688_priv, net)

petri_utils.add_arc_from_to(p18, t_4609, net)
petri_utils.add_arc_from_to(p18, t_1100, net)
petri_utils.add_arc_from_to(p18, tau_5, net)



# transition -> place
petri_utils.add_arc_from_to(t_4608, p1, net)

petri_utils.add_arc_from_to(t_4624_3, p3, net)

petri_utils.add_arc_from_to(t_4634_3, p18, net)

petri_utils.add_arc_from_to(t_1100, pSink, net)

petri_utils.add_arc_from_to(t_4609, pSink, net)

petri_utils.add_arc_from_to(t_4624_9, p10, net)
petri_utils.add_arc_from_to(t_4624_8, p5, net)
petri_utils.add_arc_from_to(t_4624_2, p5, net)
petri_utils.add_arc_from_to(t_4624_7, p5, net)

petri_utils.add_arc_from_to(t_4800, p8, net)
petri_utils.add_arc_from_to(t_4801, p7, net)

petri_utils.add_arc_from_to(t_4624_4, p12, net)
petri_utils.add_arc_from_to(t_4634_4, p11, net)

petri_utils.add_arc_from_to(t_4624_5, p14, net)
petri_utils.add_arc_from_to(t_4634_5, p11, net)

petri_utils.add_arc_from_to(t_4672, p11, net)
petri_utils.add_arc_from_to(t_4672_3, p4, net)
petri_utils.add_arc_from_to(t_4672_4, p13, net)
petri_utils.add_arc_from_to(t_4672_5, p15, net)

petri_utils.add_arc_from_to(t_4688_cmd, p16, net)
petri_utils.add_arc_from_to(t_4688_conhost, p17, net)


petri_utils.add_arc_from_to(t_4688_priv, p6, net)
petri_utils.add_arc_from_to(t_4688_unpriv, p6, net)

petri_utils.add_arc_from_to(t_4634_2_7_8_9, p18, net)

petri_utils.add_arc_from_to(tau_1, p10, net)
petri_utils.add_arc_from_to(tau_2, p9, net)
petri_utils.add_arc_from_to(tau_3, p17, net)
petri_utils.add_arc_from_to(tau_4, p7, net)
petri_utils.add_arc_from_to(tau_5, p1, net)
petri_utils.add_arc_from_to(tau_6, p2, net)
petri_utils.add_arc_from_to(tau_7, p2, net)
petri_utils.add_arc_from_to(tau_8, p6, net)
petri_utils.add_arc_from_to(tau_9, p4, net)
petri_utils.add_arc_from_to(tau_10, p13, net)


# Markings
im = Marking()
im[pSource] = 1

fm = Marking()
fm[pSink] = 1


gviz = pn_visualizer.apply(net, im, fm)
pn_visualizer.view(gviz)

# export PNML
out_dir = "Scripts/Phase_1/pnml"
os.makedirs(out_dir, exist_ok=True)
pnml_path = os.path.join(out_dir, pnml_name)
pnml_exporter.apply(net, im, pnml_path, final_marking=fm)

print(f"PNML written to: {pnml_path}")

PNML_PATH = "Scripts/Phase_1/pnml/phase_1_benign.pnml"

def get_benign_pn():
    pnml_path = Path(PNML_PATH).expanduser().resolve()

    if not pnml_path.is_file():
        raise FileNotFoundError(f"PNML file not found: {PNML_PATH}")

    net, initial_marking, final_marking = pnml_importer.apply(str(PNML_PATH))
    return net, initial_marking, final_marking

