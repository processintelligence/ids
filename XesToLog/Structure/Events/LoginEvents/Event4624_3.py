from dataclasses import dataclass
from Structure.Events.Event4624 import Event4624

@dataclass
class Event4624_3(Event4624):
    def __post_init__(self):
        self.logon_type = 3
