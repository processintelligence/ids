from dataclasses import dataclass
from Structure.Events.Event4624 import Event4624

@dataclass
class Event4624_9(Event4624):
    def __post_init__(self):
        super().__post_init__()
        self.logon_type = 9
