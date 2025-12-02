from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4648(WindowsEvent):
    account_name_new: str | None = None
    account_domain_new: str | None = None
    target_server: str | None = None
    process_id: int | None = None
    process_name: str | None = None
