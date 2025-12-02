from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4625(WindowsEvent):
    logon_type: int | None = None
    failure_reason: str | None = None
    process_id: int | None = None
    process_name: str | None = None
