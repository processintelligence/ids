from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4656(WindowsEvent):
    object_server: str
    object_type: str
    object_name: str
    handle_id: str
    process_id: int
    process_name: str
    accesses: list[str]
