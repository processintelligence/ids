from dataclasses import dataclass
from Structure import Event

@dataclass
class WindowsEvent(Event):
    username: str
    loghost: str
    domainname: str

    #should have an explanation? - explanation: str