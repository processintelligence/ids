from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4634(WindowsEvent):
    logon_type: int | None = None

    def __post_init__(self):
        self.activity_id = 4634
