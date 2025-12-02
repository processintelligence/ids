from dataclasses import dataclass
from Structure.WindowsEvent import WindowsEvent

@dataclass
class Event4648(WindowsEvent):
    account_name_new: str
    account_domain_new: str
    target_server: str
    process_id: int
    process_name: str
