from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4634(WindowsEvent):
    logon_type: int
