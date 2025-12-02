from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4657(WindowsEvent):
    object_server: str | None = None
    object_type: str | None = None
    object_name: str | None = None
    handle_id: str | None = None
    process_id: int | None = None
    process_name: str | None = None
    accesses: list[str] | None = None

    def __post_init__(self):
        self.activity_id = 4657
