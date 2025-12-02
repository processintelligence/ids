from datetime import datetime
from dataclasses import dataclass

@dataclass
class Event:
    time: datetime
    activity_id: str
    logon_id: str



