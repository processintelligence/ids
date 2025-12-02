import xml.etree.ElementTree as ET
from datetime import datetime
from EventFactory import EventFactory

#THIS SHOULD BE REWRITTEN WHEN WE START ACCEPTING STRINGS AS SUFFIX
def parse_label(label: str):
    #use method to map label to tuple, fx. 4624_2 is actually 4624 with login type 2
    if "_" in label:
        event_str, suffix = label.split("_", 1)
        try:
            event_id = int(event_str)
        except ValueError:
            return None, None

        try:
            logon_type = int(suffix)
        except ValueError:
            return event_id, None

        return event_id, logon_type

    try:
        return int(label), None
    except ValueError:
        return None, None

def placeholder_fields():
    now = datetime.now()
    return {
        "time": now,
    }

def event_from_label(label):
    #this method takes a label and creates a logline - NOT AT ALL FINISHED JUST FOR TEST

    # Skip tau/init_t and similar non-Windows transitions
    if not label[0].isdigit():
        return None

    event_id, logon_type = parse_label(label)
    fields = placeholder_fields()
    if logon_type is not None:
        fields["logon_type"] = logon_type

    return EventFactory.create(event_id, **fields)

def xes_to_event_traces(path: str):
    tree = ET.parse(path)
    root = tree.getroot()

    # handle optional XML namespace
    if "}" in root.tag:
        ns_uri = root.tag.split("}")[0].strip("{")
        ns = {"xes": ns_uri}
        trace_tag = "xes:trace"
        event_tag = "xes:event"
        string_tag = "xes:string"
    else:
        ns = {}
        trace_tag = "trace"
        event_tag = "event"
        string_tag = "string"

    traces: list[list[object]] = []

    for trace_el in root.findall(trace_tag, ns):
        events = []
        for ev_el in trace_el.findall(event_tag, ns):
            name_el = None
            for child in ev_el.findall(string_tag, ns):
                if child.attrib.get("key") == "concept:name":
                    name_el = child
                    break

            if name_el is None:
                continue

            label = name_el.attrib["value"]
            evt = event_from_label(label)
            if evt is not None:
                events.append(evt)

        traces.append(events)

    return traces

if __name__ == "__main__":
    xes_path = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/Personal/data_phase_1_net.xes"
    traces = xes_to_event_traces(xes_path)

    max_events = 100
    printed = 0
    stop = False

    for i, trace in enumerate(traces, start=1):
        if stop:
            break

        print(f"Trace {i}:")
        for e in trace:
            print("  " + e.csv_print(), end="")
            printed += 1
            if printed >= max_events:
                stop = True
                break



