from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4624(WindowsEvent):
    logon_type: int
    process_id: int
    process_name: str
    elevated_token: bool
    impersonation_level: str
