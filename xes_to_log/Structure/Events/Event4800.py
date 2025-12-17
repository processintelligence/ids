from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4800(WindowsEvent):
    pass

    def __post_init__(self):
        self.activity_id = 4800
