import sys
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.visualization.petri_net import visualizer as pn_vis


def plot_pnml(pnml_path: str) -> None:
    net, im, fm = pnml_importer.apply(pnml_path)
    gviz = pn_vis.apply(net, im, fm)
    pn_vis.view(gviz)


if __name__ == "__main__":
    path = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/heuristics_test1.pnml"

    plot_pnml(path)
    
