from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4624(WindowsEvent):
    logon_type: int | None = None
    process_id: int | None = None
    process_name: str | None = None
    elevated_token: bool | None = None
    impersonation_level: str | None = None

    def __post_init__(self):
        self.activity_id = 4624
