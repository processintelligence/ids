from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4688(WindowsEvent):
    process_id: int | None = None
    process_name: str | None = None
    token_elevation_type: str | None = None
    mandatory_level: str | None = None
    creator_process_name: str | None = None
    creator_process_id: int | None = None

    def __post_init__(self):
        self.activity_id = 4688
