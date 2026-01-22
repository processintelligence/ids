import sys
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_vis


def plot_pnml(pnml_path):
    net, im, fm = pnml_importer.apply(pnml_path)
    gviz = pn_vis.apply(net, im, fm)
    pn_vis.view(gviz)


if __name__ == "__main__":
    path = "Scripts/Phase_2/PetriNet/pnml/phase_2_redflag.pnml"

    plot_pnml(path)
    