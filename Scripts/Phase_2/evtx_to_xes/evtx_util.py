import pandas as pd
from Evtx.Evtx import Evtx
from lxml import etree
import math
import pm4py
from pm4py.objects.conversion.log import converter as log_converter

def _parse_event_xml(xml_string):
    event_dict = {}

    root = etree.fromstring(xml_string.encode("utf-8"))

    system = root.find(".//{*}System")
    if system is not None:
        for child in system:
            tag = child.tag.split("}", 1)[-1]
            if child.text and child.text.strip():
                event_dict[tag] = child.text.strip()
            for attr, val in child.attrib.items():
                event_dict[f"{tag}.{attr}"] = val

    eventdata = root.find(".//{*}EventData")
    if eventdata is not None:
        for data in eventdata.findall(".//{*}Data"):
            key = data.get("Name", "UnnamedField")
            value = data.text.strip() if data.text else None
            event_dict[f"EventData.{key}"] = value

    userdata = root.find(".//{*}UserData")
    if userdata is not None:
        for elem in userdata.iter():
            if elem is userdata:
                continue
            tag = elem.tag.split("}", 1)[-1]
            value = elem.text.strip() if elem.text else None
            event_dict[f"UserData.{tag}"] = value

    return event_dict

def evtx_to_csv(evtx_path, csv_out):
    rows = []

    with Evtx(evtx_path) as log:
        for record in log.records():
            xml = record.xml()
            event_dict = _parse_event_xml(xml)
            rows.append(event_dict)

    df = pd.DataFrame(rows)
    df.to_csv(csv_out, index=False)
    print(f"CSV written to {csv_out}")

def _is_nan_value(v):
    if v is None:
        return False
    if isinstance(v, float) and math.isnan(v):
        return True
    if isinstance(v, str) and v.lower() == "nan":
        return True
    return False

def csv_to_xes(csv_path, xes_out):
    df = pd.read_csv(csv_path)

    required = ["TimeCreated.SystemTime", "EventID", "EventData.SubjectLogonId"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")

    df = df.copy()

    df["case:concept:name"] = df["EventData.SubjectLogonId"]
    df["time:timestamp"] = pd.to_datetime(
        df["TimeCreated.SystemTime"], errors="coerce"
    )
    df["concept:name"] = df["EventID"]

    # drop events missing case id, timestamp, or activity
    df = df.dropna(subset=["case:concept:name", "time:timestamp", "concept:name"])

    # cast core fields to string
    df["case:concept:name"] = df["case:concept:name"].astype(str)
    df["concept:name"] = df["concept:name"].astype(str)

    event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)

    # remove NaN / "nan" attributes from traces and events
    for trace in event_log:
        keys_to_del = [k for k, v in trace.attributes.items() if _is_nan_value(v)]
        for k in keys_to_del:
            del trace.attributes[k]

        for event in trace:
            keys_to_del = [k for k, v in event.items() if _is_nan_value(v)]
            for k in keys_to_del:
                del event[k]

    pm4py.write_xes(event_log, xes_out)

def csv_to_xes_time_windows(csv_path, xes_out, windows,
                            timestamp_col="TimeCreated.SystemTime"):
    df = pd.read_csv(csv_path)

    if timestamp_col not in df.columns:
        raise ValueError(f"Timestamp column '{timestamp_col}' not in CSV.")

    df = df.copy()

    # Parse as UTC, then drop timezone to make them tz-naive
    df["time:timestamp"] = (
        pd.to_datetime(df[timestamp_col], errors="coerce", utc=True)
          .dt.tz_convert(None)
    )

    df = df.dropna(subset=["time:timestamp"])

    pieces = []
    for i, (start, end) in enumerate(windows, start=1):
        start_ts = pd.to_datetime(start)  # naive
        end_ts = pd.to_datetime(end)      # naive

        mask = (df["time:timestamp"] >= start_ts) & (df["time:timestamp"] <= end_ts)
        sub = df.loc[mask].copy()
        if sub.empty:
            continue

        sub["case:concept:name"] = f"trace_{i}"
        sub["concept:name"] = sub["EventID"].astype(str)

        pieces.append(sub)

    if not pieces:
        raise ValueError("No events fell into any of the given time windows.")

    df_traces = pd.concat(pieces, ignore_index=True)

    df_traces["case:concept:name"] = df_traces["case:concept:name"].astype(str)
    df_traces["concept:name"] = df_traces["concept:name"].astype(str)

    event_log = log_converter.apply(df_traces, variant=log_converter.Variants.TO_EVENT_LOG)

    for trace in event_log:
        keys_to_del = [k for k, v in trace.attributes.items() if _is_nan_value(v)]
        for k in keys_to_del:
            del trace.attributes[k]

        for event in trace:
            keys_to_del = [k for k, v in event.items() if _is_nan_value(v)]
            for k in keys_to_del:
                del event[k]

    pm4py.write_xes(event_log, xes_out)


if __name__ == "__main__":
    EVTX_FILE = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/Personal/testlog.evtx"
    CSV_OUT = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/evtx_csv/evtx_csv.csv"
    XES_OUT = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/csv_xes.xes"
    XES_OUT_TIMED = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/csv_xes_time_window.xes"

    evtx_to_csv(EVTX_FILE, CSV_OUT)
    csv_to_xes(CSV_OUT, XES_OUT)

    windows = [
        ("2025-12-01 13:39:40", "2025-12-01 13:39:52"),
        ("2025-12-01 13:40:49", "2025-12-01 13:40:59"),
        ("2025-12-01 13:41:01", "2025-12-01 13:41:16"),
    ]

    csv_to_xes_time_windows(CSV_OUT, XES_OUT_TIMED, windows)

