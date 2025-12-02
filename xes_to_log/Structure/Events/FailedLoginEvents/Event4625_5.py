from dataclasses import dataclass
from Structure.Events.Event4625 import Event4625

@dataclass
class Event4625_5(Event4625):
    def __post_init__(self):
        self.logon_type = 5
