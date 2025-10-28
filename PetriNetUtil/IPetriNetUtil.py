from abc import ABC, abstractmethod
from typing import Tuple
from pm4py.objects.petri_net.obj import PetriNet, Marking


class IPetriNetUtil(ABC):
    @abstractmethod
    def get_petrinet(
        self,
        pnml_path: str
        ) -> Tuple[PetriNet, Marking, Marking]:
        pass

    @abstractmethod
    def create_blanc_config(
        self,
        petrinet: PetriNet,
        output_path: str,
        save_to_disk: bool
    ) -> dict:
        pass

    @abstractmethod
    def validate_config(
        self,
        config: str
    ) -> bool:
        pass

    @abstractmethod
    def obtain_guards(
        self,
        petrinet: PetriNet,
        config: str
        ) -> str:
        pass

    @abstractmethod
    def combine_guards(
        self,
        pre_conditions: dict,
        post_conditions: dict,
        ) -> dict:
        pass
    
    @abstractmethod
    def create_data_pnml(
        self,
        guards: dict,
        pnml_path: str
        ) -> str:
        pass