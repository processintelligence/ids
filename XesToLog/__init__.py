from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    time: datetime
    activity_id: str
    logon_id: str


@dataclass
class WindowsEvent(Event):
    """
    Windows-specific event extending the base Event structure.
    """
    username: str
    loghost: str
    domainname: str
