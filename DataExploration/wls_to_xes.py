import json
import xml.etree.ElementTree as ET
import datetime
from collections import Counter

# CONVERT LOS ALAMOS DATA TO XES
# Divide login type and processes into sub-events

INPUT_FILE = "C:/Users/lomo0/Downloads/wls_day-01" #TODO: input correct files 
OUTPUT_FILE = "C:/Users/lomo0/Downloads/wls_full.xes"

# XES setup
xes_ns = "http://www.xes-standard.org/"
ET.register_namespace("", xes_ns) 

log = ET.Element(
    "{http://www.xes-standard.org/}log",
    {
        "xes.version": "1.0",
        "xes.features": "nested-attributes"
    }
)

ET.SubElement(log, "{http://www.xes-standard.org/}extension", {
    "name": "Concept",
    "prefix": "concept",
    "uri": "http://www.xes-standard.org/concept.xesext"
})
ET.SubElement(log, "{http://www.xes-standard.org/}extension", {
    "name": "Time",
    "prefix": "time",
    "uri": "http://www.xes-standard.org/time.xesext"
})
ET.SubElement(log, "{http://www.xes-standard.org/}classifier", {
    "name": "Activity classifier",
    "keys": "concept:name"
})

traces = {}
all_4688_events = []

# Read and process JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line_no, line in enumerate(f, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Error on line {line_no}: {e}")
            continue

        username = data.get("UserName")
        logonid = data.get("LogonID")
        activity = data.get("EventID")
        timestamp = data.get("Time")
        logontype = data.get("LogonType")
        process_name = data.get("ProcessName") 

        # Skip invalid entries and non-user traces
        if username is None or logonid is None or activity is None or timestamp is None:
            continue
        if not username.startswith("User"):
            continue

        # Include login type and process name in activity
        if activity in [4624, 4634] and logontype is not None:
            activity_name = f"{activity}_{logontype}"
        elif activity == 4688 and process_name:
            activity_name = f"{activity}_{process_name}"
            all_4688_events.append(activity_name) 
        else:
            activity_name = str(activity)
        try:
            ts_str = datetime.datetime.fromtimestamp(float(timestamp)).isoformat()
        except Exception:
            ts_str = str(timestamp)

        case_id = str(logonid)
        if case_id not in traces:
            traces[case_id] = []
        traces[case_id].append((activity_name, ts_str))

# Filter infrequent 4688 events
event_counts = Counter(all_4688_events)
frequent_4688 = {evt for evt, count in event_counts.items() if count >= 10}

for case_id in list(traces.keys()):
    filtered_events = []
    for activity, ts_str in traces[case_id]:
        if activity.startswith("4688_") and activity not in frequent_4688:
            continue  
        filtered_events.append((activity, ts_str))
    traces[case_id] = filtered_events

filtered_traces = {cid: evts for cid, evts in traces.items() if 2 <= len(evts) < 10}
removed_count = len(traces) - len(filtered_traces)
print(f"Removed {removed_count} traces")
print(f"Remaining traces: {len(filtered_traces)}")

def indent(elem, level=0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

# Insert traces into XES
for case_id, events in filtered_traces.items():
    trace = ET.SubElement(log, "trace")
    ET.SubElement(trace, "string", {"key": "concept:name", "value": case_id})
    ET.SubElement(trace, "string", {"key": "case:concept:name", "value": case_id})
    for activity, ts_str in events:
        event = ET.SubElement(trace, "event")
        ET.SubElement(event, "string", {"key": "concept:name", "value": activity})
        ET.SubElement(event, "date", {"key": "time:timestamp", "value": ts_str})

indent(log)
tree = ET.ElementTree(log)
tree.write(OUTPUT_FILE, encoding="UTF-8", xml_declaration=True)
