from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4672(WindowsEvent):
    privileges: list[str] | None = None
    # e.g. ["SeDebugPrivilege", "SeBackupPrivilege"]

    def __post_init__(self):
        self.activity_id = 4672
