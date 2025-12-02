from dataclasses import dataclass
from Structure.Event import Event

@dataclass
class WindowsEvent(Event):
    username: str
    loghost: str
    domainname: str