from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4625(WindowsEvent):
    logon_type: int
    failure_reason: str
    process_id: int
    process_name: str
