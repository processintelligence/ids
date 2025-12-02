from dataclasses import dataclass
from Structure.Events.Event4625 import Event4625

@dataclass
class Event4625_7(Event4625):
    def __post_init__(self):
        super().__post_init__()
        self.logon_type = 7
