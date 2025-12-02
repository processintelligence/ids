from datetime import datetime

from Structure.Events.Event4608 import Event4608
from Structure.Events.Event4609 import Event4609
from Structure.Events.Event1100 import Event1100

from Structure.Events.Event4624 import Event4624
from Structure.Events.LoginEvents.Event4624_2 import Event4624_2
from Structure.Events.LoginEvents.Event4624_3 import Event4624_3
from Structure.Events.LoginEvents.Event4624_4 import Event4624_4
from Structure.Events.LoginEvents.Event4624_5 import Event4624_5
from Structure.Events.LoginEvents.Event4624_7 import Event4624_7
from Structure.Events.LoginEvents.Event4624_8 import Event4624_8
from Structure.Events.LoginEvents.Event4624_9 import Event4624_9

from Structure.Events.Event4625 import Event4625
from Structure.Events.FailedLoginEvents.Event4625_2 import Event4625_2
from Structure.Events.FailedLoginEvents.Event4625_3 import Event4625_3
from Structure.Events.FailedLoginEvents.Event4625_4 import Event4625_4
from Structure.Events.FailedLoginEvents.Event4625_5 import Event4625_5
from Structure.Events.FailedLoginEvents.Event4625_7 import Event4625_7
from Structure.Events.FailedLoginEvents.Event4625_8 import Event4625_8
from Structure.Events.FailedLoginEvents.Event4625_9 import Event4625_9

from Structure.Events.Event4634 import Event4634
from Structure.Events.LogoutEvents.Event4634_2 import Event4634_2
from Structure.Events.LogoutEvents.Event4634_3 import Event4634_3
from Structure.Events.LogoutEvents.Event4634_4 import Event4634_4
from Structure.Events.LogoutEvents.Event4634_5 import Event4634_5
from Structure.Events.LogoutEvents.Event4634_7 import Event4634_7
from Structure.Events.LogoutEvents.Event4634_8 import Event4634_8
from Structure.Events.LogoutEvents.Event4634_9 import Event4634_9

from Structure.Events.Event4672 import Event4672
from Structure.Events.Event4688 import Event4688
from Structure.Events.Event4800 import Event4800
from Structure.Events.Event4801 import Event4801
from Structure.Events.Event4656 import Event4656
from Structure.Events.Event4663 import Event4663
from Structure.Events.Event4657 import Event4657
from Structure.Events.Event4658 import Event4658


class EventFactory:
    _subclasses = {
        4624: {
            2: Event4624_2,
            3: Event4624_3,
            4: Event4624_4,
            5: Event4624_5,
            7: Event4624_7,
            8: Event4624_8,
            9: Event4624_9,
        },
        4625: {
            2: Event4625_2,
            3: Event4625_3,
            4: Event4625_4,
            5: Event4625_5,
            7: Event4625_7,
            8: Event4625_8,
            9: Event4625_9,
        },
        4634: {
            2: Event4634_2,
            3: Event4634_3,
            4: Event4634_4,
            5: Event4634_5,
            7: Event4634_7,
            8: Event4634_8,
            9: Event4634_9,
        },
    }

    _base = {
        4608: Event4608,
        4609: Event4609,
        1100: Event1100,
        4624: Event4624,
        4625: Event4625,
        4634: Event4634,
        4672: Event4672,
        4688: Event4688,
        4800: Event4800,
        4801: Event4801,
        4656: Event4656,
        4663: Event4663,
        4657: Event4657,
        4658: Event4658,
    }

    @staticmethod
    def create(event_id, **kwargs):
        subclasses = EventFactory._subclasses.get(event_id)
        if subclasses is not None:
            logon_type = kwargs.get("logon_type")
            if logon_type is not None:
                cls = subclasses.get(logon_type)
                if cls is not None:
                    return cls(**kwargs)

        base_cls = EventFactory._base.get(event_id)
        if base_cls is None:
            return None

        if event_id not in EventFactory._subclasses:
            kwargs.pop("logon_type", None)

        return base_cls(**kwargs)


if __name__ == "__main__":
    fields_4624_3 = {
        "time": datetime.now(),
        "activity_id": "abc-123",
        "logon_id": "0xdeadbeef",
        "username": "Emil",
        "loghost": "DESKTOP-01",
        "domainname": "CORP",
        "process_id": 1234,
        "process_name": "winlogon.exe",
        "elevated_token": False,
        "impersonation_level": "None",
        "logon_type": 3,
    }

    event_4624_3 = EventFactory.create(4624, **fields_4624_3)
    print(type(event_4624_3))
    print(event_4624_3)

    fields_4688 = {
        "time": datetime.now(),
        "activity_id": "xyz-999",
        "logon_id": "0x123",
        "username": "Emil",
        "loghost": "DESKTOP-01",
        "domainname": "CORP",
        "process_id": 5678,
        "process_name": "cmd.exe",
        "creator_process_id": 1111,
        "creator_process_name": "explorer.exe",
    }

    event_4688 = EventFactory.create(4688, **fields_4688)
    print(type(event_4688))
    print(event_4688)

