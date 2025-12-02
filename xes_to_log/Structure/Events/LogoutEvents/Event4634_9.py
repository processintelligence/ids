from dataclasses import dataclass
from Structure.Events.Event4634 import Event4634

@dataclass
class Event4634_9(Event4634):
    def __post_init__(self):
        self.logon_type = 9
