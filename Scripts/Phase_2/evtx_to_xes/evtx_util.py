import pandas as pd
from Evtx.Evtx import Evtx
from lxml import etree
import math
import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.obj import EventLog, Trace
import os

def _is_nan_value(v):
    if v is None:
        return False
    if isinstance(v, float) and math.isnan(v):
        return True
    if isinstance(v, str) and v.lower() == "nan":
        return True
    return False

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

def evtx_list_to_csv(evtx_paths, csv_out):
    rows = []

    for evtx_path in evtx_paths:
        with Evtx(evtx_path) as log:
            for record in log.records():
                xml = record.xml()
                event_dict = _parse_event_xml(xml)
                event_dict["__source_evtx"] = os.path.basename(evtx_path)
                rows.append(event_dict)

    df = pd.DataFrame(rows)
    df.to_csv(csv_out, index=False)
    print(f"Combined CSV written to {csv_out} from {len(evtx_paths)} EVTX files")

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

    df = df.dropna(subset=["case:concept:name", "time:timestamp", "concept:name"])

    df["case:concept:name"] = df["case:concept:name"].astype(str)
    df["concept:name"] = df["concept:name"].astype(str)

    event_log = log_converter.apply(df, variant=log_converter.Variants.TO_EVENT_LOG)

    for trace in event_log:
        keys_to_del = [k for k, v in trace.attributes.items() if _is_nan_value(v)]
        for k in keys_to_del:
            del trace.attributes[k]

        for event in trace:
            keys_to_del = [k for k, v in event.items() if _is_nan_value(v)]
            for k in keys_to_del:
                del event[k]

    pm4py.write_xes(event_log, xes_out)

def csv_to_xes_time_windows(csv_path, xes_out, windows, timestamp_col="TimeCreated.SystemTime"):
    df = pd.read_csv(csv_path)

    if timestamp_col not in df.columns:
        raise ValueError(f"Timestamp column '{timestamp_col}' not in CSV.")

    df = df.copy()

    df["time:timestamp"] = (
        pd.to_datetime(df[timestamp_col], errors="coerce", utc=True)
          .dt.tz_convert(None)
    )

    df = df.dropna(subset=["time:timestamp"])

    pieces = []
    for i, (start, end) in enumerate(windows, start=1):
        start_ts = pd.to_datetime(start, utc=True).tz_convert(None)
        end_ts = pd.to_datetime(end, utc=True).tz_convert(None)

        # strictly between FuzzStarter and FuzzEnder
        mask = (df["time:timestamp"] > start_ts) & (df["time:timestamp"] < end_ts)
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

    event_log = enrich_event_ids(event_log)
    event_log = drop_leading(event_log)
    event_log = drop_trailing(event_log)
    pm4py.write_xes(event_log, xes_out)



def get_fuzz_time_windows_from_csv(csv_path, timestamp_col="TimeCreated.SystemTime", object_col="EventData.ObjectName", eventid_col="EventID", start_substring="FuzzStarter", end_substring="FuzzEnder", start_eventid=4663, end_eventid=None):

        df = pd.read_csv(csv_path)

        for col in (timestamp_col, object_col, eventid_col):
            if col not in df.columns:
                raise ValueError(f"Required column '{col}' not found in CSV.")

        df = df.copy()
        df["_parsed_ts"] = pd.to_datetime(df[timestamp_col], errors="coerce", utc=True)
        df = df.dropna(subset=["_parsed_ts"])

        df = df.sort_values("_parsed_ts")

        windows = []
        current_start = None

        for _, row in df.iterrows():
            obj_val = row[object_col]
            obj = "" if _is_nan_value(obj_val) else str(obj_val)
            eventid = row[eventid_col]
            ts = row["_parsed_ts"]

            # START condition: FuzzStarter + EventID == 4663
            if start_substring in obj and eventid == start_eventid:
                current_start = ts

            # END condition: first FuzzEnder after a start
            elif end_substring in obj and (end_eventid is None or eventid == end_eventid):
                if current_start is not None:
                    windows.append((current_start.isoformat(), ts.isoformat()))
                    current_start = None

        return windows

def enrich_event_ids(event_log):
    for trace in event_log:
        for event in trace:

            raw_eid = event.get("EventID", event.get("concept:name"))
            if raw_eid is None:
                continue

            eid = str(raw_eid)
            new_name = None

            # 4624 / 4634 -> append LogonType
            if eid in ("4624", "4634"):
                lt = event.get("EventData.LogonType")
                if lt is not None and not _is_nan_value(lt):
                    if isinstance(lt, float):
                        if lt.is_integer():
                            lt_str = str(int(lt))
                        else:
                            lt_str = str(lt)
                    else:
                        s = str(lt)
                        lt_str = s[:-2] if s.endswith(".0") else s

                    new_name = f"{eid}_{lt_str}"

            # 4688 -> append NewProcessName
            elif eid == "4688":
                npn = event.get("EventData.NewProcessName")
                if npn is not None and not _is_nan_value(npn):
                    s = str(npn)
                    proc_name = s.replace("/", "\\").split("\\")[-1]
                    new_name = f"{eid}_{proc_name}"

            # 4657 -> ObjectValueName contains 'common' then append 'common' else append operationtype
            elif eid == "4657":
                obj_val = event.get("EventData.ObjectValueName")
                op_type = event.get("EventData.operationtype") or event.get("EventData.OperationType")

                has_obj_val = obj_val is not None and not _is_nan_value(obj_val)
                has_op_type = op_type is not None and not _is_nan_value(op_type)

                if has_obj_val and "common" in str(obj_val).lower():
                    new_name = f"{eid}_common"
                elif has_op_type:
                    s = str(op_type)

                    if "1905" in s:
                        op_label = "modified"
                    elif "1904" in s:
                        op_label = "created"
                    elif "1906" in s:
                        op_label = "deleted"
                    else:
                        op_label = s

                    new_name = f"{eid}_{op_label}"


            if new_name is not None:
                event["concept:name"] = str(new_name)

    return event_log


def get_eid(ev):
    raw = ev.get("EventID", ev.get("concept:name", ""))
    return str(raw) if raw is not None else ""


def drop_leading(event_log):
    new_log = EventLog(attributes=event_log.attributes)

    for trace in event_log:
        events = list(trace)
        if not events:
            continue

        drop_count = 0

        if len(events) > drop_count and get_eid(events[drop_count]).startswith("4658"):
            drop_count += 1

        if len(events) > drop_count and get_eid(events[drop_count]).startswith("4688"):
            drop_count += 1

        if len(events) > drop_count and get_eid(events[drop_count]).startswith("4688"):
            drop_count += 1

        remaining = events[drop_count:]
        if not remaining:
            continue

        new_trace = Trace(remaining, attributes=trace.attributes)
        new_log.append(new_trace)

    return new_log

def drop_trailing(event_log):
    new_log = EventLog(attributes=event_log.attributes)

    for trace in event_log:
        events = list(trace)
        if not events:
            continue

        end_idx = len(events)

        if end_idx > 0 and get_eid(events[end_idx - 1]).startswith("4658"):
            end_idx -= 1

        if end_idx > 0 and get_eid(events[end_idx - 1]).startswith("4690"):
            end_idx -= 1

        remaining = events[:end_idx]
        if not remaining:
            continue

        new_trace = Trace(remaining, attributes=trace.attributes)
        new_log.append(new_trace)

    return new_log

if __name__ == "__main__":
    EVTX_FILE1 = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/Scripts/Phase_2/evtx_files/300Scripts1_backup.evtx"
    EVTX_FILE2 = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/Scripts/Phase_2/evtx_files/300Scripts2_backup.evtx"
    EVTX_FILE3 = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/Scripts/Phase_2/evtx_to_xes/evtx_files/300Scripts3_backup.evtx"

    evtx_files = [EVTX_FILE1, EVTX_FILE2, EVTX_FILE3]

    CSV_OUT = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/evtx_csv/evtx_csv_1000.csv"
    XES_OUT = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/csv_xes_time_window.xes"

    evtx_list_to_csv(evtx_files, CSV_OUT)
    windows = get_fuzz_time_windows_from_csv(CSV_OUT)
    csv_to_xes_time_windows(CSV_OUT, XES_OUT, windows)

    print("Generated XES from combined EVTX files")
