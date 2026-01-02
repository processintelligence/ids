from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.visualization.petri_net import visualizer as pn_visualizer
import os



def build_attack_petri_net_new_version():
    net = PetriNet("attack_petri_net")

    # Places
    p1 = PetriNet.Place("p1")
    p2 = PetriNet.Place("p2")
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
    p19 = PetriNet.Place("p19")
    p20 = PetriNet.Place("p20")
    p21 = PetriNet.Place("p21")
    p22 = PetriNet.Place("p22")
    p23 = PetriNet.Place("p23")
    p24 = PetriNet.Place("p24")

    net.places.update({
        p1, p2, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13,
        p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24
    })

    # Transitions
    t_4608 = PetriNet.Transition("4608", "4608")
    t_4624_3 = PetriNet.Transition("4624_3", "4624_3")
    t_4634_3 = PetriNet.Transition("4634_3", "4634_3")
    t_4625_9_8_2_7_3 = PetriNet.Transition("4625_9_8_2_7_3", "4625_9_8_2_7_3")
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
    t_4625_4_5 = PetriNet.Transition("4625_4_5", "4625_4_5")

    t_4672 = PetriNet.Transition("4672", "4672")
    t_4672_3 = PetriNet.Transition("4672_3", "4672_3")
    t_4672_4 = PetriNet.Transition("4672_4", "4672_4")
    t_4672_5 = PetriNet.Transition("4672_5", "4672_5")

    t_4688_cmd = PetriNet.Transition("4688_cmd", "4688_cmd")
    t_4688_conhost = PetriNet.Transition("4688_conhost", "4688_conhost")
    t_4648 = PetriNet.Transition("4648", "4648")
    t_4688_priv = PetriNet.Transition("4688_priv", "4688_priv")
    t_4688_unpriv = PetriNet.Transition("4688_unpriv", "4688_unpriv")

    t_4656 = PetriNet.Transition("4656", "4656")
    t_4663 = PetriNet.Transition("4663", "4663")
    t_4657_common = PetriNet.Transition("4657_common", "4657_common")
    t_4657_registry = PetriNet.Transition("4657_registry", "4657_registry")
    t_4658 = PetriNet.Transition("4658", "4658")

    #PetriNet.Transition(name, label), set label as None to allow silent 
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
    tau_11 = PetriNet.Transition("tau_11", None)
    tau_12 = PetriNet.Transition("tau_12", None)
    tau_13 = PetriNet.Transition("tau_13", None)
    """
    tau_1 = PetriNet.Transition("tau_1", "tau_1")
    tau_2 = PetriNet.Transition("tau_2", "tau_2")
    tau_3 = PetriNet.Transition("tau_3", "tau_3")
    tau_4 = PetriNet.Transition("tau_4", "tau_4")
    tau_5 = PetriNet.Transition("tau_5", "tau_5")
    tau_6 = PetriNet.Transition("tau_6", "tau_6")
    tau_7 = PetriNet.Transition("tau_7", "tau_7")
    tau_8 = PetriNet.Transition("tau_8", "tau_8")
    tau_9 = PetriNet.Transition("tau_9", "tau_9")
    tau_10 = PetriNet.Transition("tau_10", "tau_10")
    tau_11 = PetriNet.Transition("tau_11", "tau_11")
    tau_12 = PetriNet.Transition("tau_12", "tau_12")
    tau_13 = PetriNet.Transition("tau_13", "tau_13")
    """

    net.transitions.update({
        t_4608, t_4624_3, t_4634_3, t_4625_9_8_2_7_3, t_1100, t_4609,
        t_4624_9, t_4624_8, t_4624_2, t_4624_7, t_4634_2_7_8_9,
        t_4800, t_4801,
        t_4624_4, t_4634_4, t_4634_5, t_4624_5, t_4625_4_5,
        t_4672, t_4672_3, t_4672_4, t_4672_5,
        t_4688_cmd, t_4688_conhost, t_4648, t_4688_priv, t_4688_unpriv,
        t_4656, t_4663, t_4657_common, t_4657_registry, t_4658,
        tau_1, tau_2, tau_3, tau_4, tau_5, tau_6, tau_7, tau_8, tau_9, tau_10, tau_11, tau_12, tau_13
    })


    # place -> transition
    petri_utils.add_arc_from_to(p1, t_4608, net)

    petri_utils.add_arc_from_to(p2, t_4672_3, net)
    petri_utils.add_arc_from_to(p2, tau_11, net)

    petri_utils.add_arc_from_to(p4, t_4624_9, net)
    petri_utils.add_arc_from_to(p4, t_4624_8, net)
    petri_utils.add_arc_from_to(p4, t_4624_2, net)
    petri_utils.add_arc_from_to(p4, t_4624_7, net)
    petri_utils.add_arc_from_to(p4, tau_8, net)
    petri_utils.add_arc_from_to(p4, t_4625_9_8_2_7_3, net)

    petri_utils.add_arc_from_to(p5, t_4672, net)

    petri_utils.add_arc_from_to(p6, tau_1, net)
    petri_utils.add_arc_from_to(p6, t_4800, net)
    petri_utils.add_arc_from_to(p6, tau_2, net)
    petri_utils.add_arc_from_to(p6, t_4648, net)

    petri_utils.add_arc_from_to(p7, t_4801, net)

    petri_utils.add_arc_from_to(p8, t_4672_5, net)
    petri_utils.add_arc_from_to(p8, tau_13, net)

    petri_utils.add_arc_from_to(p9, t_4624_5, net)
    petri_utils.add_arc_from_to(p9, t_4624_4, net)
    petri_utils.add_arc_from_to(p9, t_4625_4_5, net)
    petri_utils.add_arc_from_to(p9, tau_3, net)
    petri_utils.add_arc_from_to(p9, tau_9, net)
    petri_utils.add_arc_from_to(p9, t_4688_cmd, net)

    petri_utils.add_arc_from_to(p10, t_4688_priv, net)
    petri_utils.add_arc_from_to(p10, t_4656, net)

    petri_utils.add_arc_from_to(p11, t_4663, net)
    petri_utils.add_arc_from_to(p11, tau_4, net)

    petri_utils.add_arc_from_to(p12, t_4688_unpriv, net)

    petri_utils.add_arc_from_to(p13, t_4688_conhost, net)

    petri_utils.add_arc_from_to(p14, tau_5, net)
    petri_utils.add_arc_from_to(p14, t_4657_common, net)
    petri_utils.add_arc_from_to(p14, t_4657_registry, net)

    petri_utils.add_arc_from_to(p15, t_4658, net)

    petri_utils.add_arc_from_to(p16, tau_6, net)
    petri_utils.add_arc_from_to(p16, t_4634_2_7_8_9, net)

    petri_utils.add_arc_from_to(p18, t_4609, net)
    petri_utils.add_arc_from_to(p18, t_1100, net)
    petri_utils.add_arc_from_to(p18, tau_7, net)

    petri_utils.add_arc_from_to(p19, t_4672_4, net)
    petri_utils.add_arc_from_to(p19, tau_12, net)

    petri_utils.add_arc_from_to(p20, t_4624_3, net)

    petri_utils.add_arc_from_to(p21, tau_10, net)

    petri_utils.add_arc_from_to(p22, t_4634_3, net)

    petri_utils.add_arc_from_to(p23, t_4634_4, net)

    petri_utils.add_arc_from_to(p24, t_4634_5, net)

    # transition -> place
    petri_utils.add_arc_from_to(t_4608, p4, net)

    petri_utils.add_arc_from_to(t_4624_3, p2, net)

    petri_utils.add_arc_from_to(t_4634_3, p18, net)

    petri_utils.add_arc_from_to(t_4625_9_8_2_7_3, p4, net)

    petri_utils.add_arc_from_to(t_1100, p17, net)
    petri_utils.add_arc_from_to(t_4609, p17, net)

    petri_utils.add_arc_from_to(t_4624_9, p5, net)

    petri_utils.add_arc_from_to(t_4624_8, p21, net)
    petri_utils.add_arc_from_to(t_4624_2, p21, net)
    petri_utils.add_arc_from_to(t_4624_7, p21, net)

    petri_utils.add_arc_from_to(tau_1, p5, net)
    petri_utils.add_arc_from_to(tau_2, p12, net)
    petri_utils.add_arc_from_to(tau_3, p10, net)
    petri_utils.add_arc_from_to(tau_4, p14, net)
    petri_utils.add_arc_from_to(tau_5, p16, net)
    petri_utils.add_arc_from_to(tau_6, p6, net)
    petri_utils.add_arc_from_to(tau_7, p4, net)
    petri_utils.add_arc_from_to(tau_8, p20, net)
    petri_utils.add_arc_from_to(tau_9, p20, net)
    petri_utils.add_arc_from_to(tau_10, p16, net)
    petri_utils.add_arc_from_to(tau_11, p22, net)
    petri_utils.add_arc_from_to(tau_12, p23, net)
    petri_utils.add_arc_from_to(tau_13, p24, net)

    petri_utils.add_arc_from_to(t_4800, p7, net)
    petri_utils.add_arc_from_to(t_4801, p6, net)

    petri_utils.add_arc_from_to(t_4624_4, p19, net)
    petri_utils.add_arc_from_to(t_4634_4, p9, net)

    petri_utils.add_arc_from_to(t_4624_5, p8, net)
    petri_utils.add_arc_from_to(t_4634_5, p9, net)

    petri_utils.add_arc_from_to(t_4625_4_5, p9, net)

    petri_utils.add_arc_from_to(t_4672, p9, net)
    petri_utils.add_arc_from_to(t_4672_3, p22, net)
    petri_utils.add_arc_from_to(t_4672_4, p23, net)
    petri_utils.add_arc_from_to(t_4672_5, p24, net)

    petri_utils.add_arc_from_to(t_4688_cmd, p13, net)
    petri_utils.add_arc_from_to(t_4688_conhost, p10, net)
    petri_utils.add_arc_from_to(t_4648, p10, net)

    petri_utils.add_arc_from_to(t_4656, p11, net)
    petri_utils.add_arc_from_to(t_4663, p14, net)

    petri_utils.add_arc_from_to(t_4657_common, p15, net)
    petri_utils.add_arc_from_to(t_4657_registry, p15, net)

    petri_utils.add_arc_from_to(t_4688_priv, p16, net)
    petri_utils.add_arc_from_to(t_4688_unpriv, p16, net)
    petri_utils.add_arc_from_to(t_4658, p16, net)

    petri_utils.add_arc_from_to(t_4634_2_7_8_9, p18, net)

    # Markings
    im = Marking()
    im[p1] = 1

    fm = Marking()
    fm[p17] = 1

    return net, im, fm


if __name__ == "__main__":
    net, im, fm = build_attack_petri_net_new_version()

    print("Places:", sorted([p.name for p in net.places]))
    print("Transitions:", sorted([t.name for t in net.transitions]))
    print("Arcs:", [(a.source.name, a.target.name) for a in net.arcs])

    gviz = pn_visualizer.apply(net, im, fm)
    pn_visualizer.view(gviz)

    # export PNML
    out_dir = "PNMLFiles"
    os.makedirs(out_dir, exist_ok=True)
    pnml_path = os.path.join(out_dir, "attack_petri_net_new.pnml")
    pnml_exporter.apply(net, im, pnml_path, final_marking=fm)

    print(f"PNML written to: {pnml_path}")
