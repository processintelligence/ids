from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4672(WindowsEvent):
    privileges: list[str]   # e.g. ["SeDebugPrivilege", "SeBackupPrivilege"]
