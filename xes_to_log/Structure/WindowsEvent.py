from dataclasses import dataclass
from Structure.Event import Event

@dataclass
class WindowsEvent(Event):
    username: str| None = None
    loghost: str | None = None
    domainname: str | None = None