from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4688(WindowsEvent):
    process_id: int
    process_name: str
    token_elevation_type: str
    mandatory_level: str
    creator_process_name: str
    creator_process_id: int
