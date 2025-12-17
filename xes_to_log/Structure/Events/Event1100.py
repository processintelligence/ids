from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event1100(WindowsEvent):
    def __post_init__(self):
        self.activity_id = 1100
