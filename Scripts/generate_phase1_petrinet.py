from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
import os

net = PetriNet("Phase_1")

#Places
places = {PetriNet.Place(f"p{i}") for i in range(1, 15)}
net.places.update(places)

#traces
t_4608 = PetriNet.Transition("t_4608", "t_4608")

t_4624_3 = PetriNet.Transition("t_4624_3", "t_4624_3")
t_4634_3 = PetriNet.Transition("t_4634_3", "t_4634_3")

t_1100 = PetriNet.Transition("t_1100", "t_1100")
t_4609 = PetriNet.Transition("t_4609", "t_4609")

t_4624_9 = PetriNet.Transition("t_4624_9", "t_4624_9")
t_4624_8 = PetriNet.Transition("t_4624_8", "t_4624_8")
t_4624_2 = PetriNet.Transition("t_4624_2", "t_4624_2")
t_4624_7 = PetriNet.Transition("t_4624_7", "t_4624_7")
t_4634_2_7_8_9 = PetriNet.Transition("t_4634_2_7_8_9", "t_4634_2_7_8_9")

t_4801 = PetriNet.Transition("t_4801", "t_462t_48014_9")
t_4800 = PetriNet.Transition("t_4800", "t_4800")

t_4624_4 = PetriNet.Transition("t_4624_4", "t_4624_4")
t_4634_4 = PetriNet.Transition("t_4634_4", "t_4634_4")

t_4634_5 = PetriNet.Transition("t_4634_5", "t_4634_5")
t_4624_5 = PetriNet.Transition("t_4624_5", "t_4624_5")

t_4672 = PetriNet.Transition("t_4672", "t_4672")
t_4688_cmd = PetriNet.Transition("t_4688_cmd", "t_4688_cmd")
t_4688_conhost = PetriNet.Transition("t_4688_conhost", "t_4688_conhost")
t_4648 = PetriNet.Transition("t_4648", "t_4648")
t_4688_priv = PetriNet.Transition("t_4688_priv", "t_4688_priv")

t_4688_unpriv = PetriNet.Transition("t_4688_unpriv", "t_4688_unpriv")



