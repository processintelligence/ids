from datetime import datetime
from dataclasses import dataclass, fields

@dataclass
class Event:
    time: datetime | None = None
    activity_id: int | None = None
    logon_id: str | None = None

    def csv_print(self) -> str:
        parts = []
        for f in fields(self):
            value = getattr(self, f.name)
            parts.append(f"{f.name}={value!r}")
        return ", ".join(parts) + "\n"
