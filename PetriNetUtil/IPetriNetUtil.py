from abc import ABC, abstractmethod
from typing import Tuple
from pm4py.objects.petri_net.obj import PetriNet, Marking


class IPetriNetUtil(ABC):
    @abstractmethod
    def generate_config_structure(self, pnml_path: str) -> str:
        pass

    @abstractmethod
    def generate_data_petrinet(self, config: str) -> str:
        pass