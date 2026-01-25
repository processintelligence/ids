import math
import os
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet, List, Optional, Sequence, Tuple
import pandas as pd
import pm4py
from Evtx.Evtx import Evtx
from lxml import etree
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.obj import EventLog, Trace

@dataclass
class LogConfig:
    # Column names expected in the CSV
    timestamp_col: str = "TimeCreated.SystemTime"
    object_col: str = "EventData.ObjectName"
    eventid_col: str = "EventID"

    start_substring: str = "FuzzStarter" # Marker to define when a trace starts
    end_substring: str = "FuzzEnder" # Markter to define when a trace ends
    start_eventid: int = 4663
    end_eventid: Optional[int] = None

    # Set of allowed 4688 events 
    allowed_4688: FrozenSet[str] = frozenset(
        {
            "4688_cmd"
        }
    )

    # Prefixes used to identify the logical start/end of a trace after enrichment.
    trace_start_prefix: str = "4624_2"
    trace_end_prefix: str = "4634_2"


def _is_nan_value(v):
    # Handle NaN values
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


def get_eid(ev):
    raw = ev.get("EventID", ev.get("concept:name", ""))
    return str(raw) if raw is not None else ""


def _matches_eventid(val, expected):
    # Checks if event ids are equal
    if expected is None:
        return True
    try:
        return int(val) == int(expected)
    except Exception:
        return str(val) == str(expected)


def _normalize_logon_id(v):
    # Normalize id for comparison
    if v is None or _is_nan_value(v):
        return None
    return str(v).strip().lower()


def _format_logon_type_value(lt):
    # Format logon types
    if lt is None or _is_nan_value(lt):
        return None

    if isinstance(lt, float):
        return str(int(lt)) if lt.is_integer() else str(lt)

    s = str(lt)
    return s[:-2] if s.endswith(".0") else s


def _normalize_handle(v):
    # Normalize id 
    """Normalize handle IDs for comparison: strip, lowercase; return None for NaN-like values."""
    if v is None or _is_nan_value(v):
        return None
    return str(v).strip().lower()


def evtx_to_csv(evtx_paths: Sequence[str], csv_out: str) -> None:
    #exports an evtx file into csv format 
    rows = []
    for evtx_path in evtx_paths:
        with Evtx(evtx_path) as log:
            for record in log.records():
                xml = record.xml()
                event_dict = _parse_event_xml(xml)
                event_dict["__source_evtx"] = os.path.basename(evtx_path)
                rows.append(event_dict)

    pd.DataFrame(rows).to_csv(csv_out, index=False)


def get_start_and_end_from_csv(csv_path, config):
    # Finds the start and end of all traces in the csv
    df = pd.read_csv(csv_path)

    required = (config.timestamp_col, config.object_col, config.eventid_col)
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in CSV.")

    df = df.copy()
    df["_parsed_ts"] = pd.to_datetime(df[config.timestamp_col], errors="coerce", utc=True)
    df = df.dropna(subset=["_parsed_ts"]).sort_values("_parsed_ts")

    windows = []
    current_start = None

    for _, row in df.iterrows():
        obj_val = row[config.object_col]
        obj = "" if _is_nan_value(obj_val) else str(obj_val)
        eventid = row[config.eventid_col]
        ts = row["_parsed_ts"]

        # Adding to windows all times of start and end 
        if config.start_substring in obj and _matches_eventid(eventid, config.start_eventid):
            current_start = ts
        elif config.end_substring in obj and _matches_eventid(eventid, config.end_eventid):
            if current_start is not None:
                windows.append((current_start.isoformat(), ts.isoformat()))
                current_start = None

    return windows


def _enrich_logon_type(event, eid):
    # enriching login ids with tids logon type 
    lt = event.get("EventData.LogonType")
    if lt is None or _is_nan_value(lt):
        return None

    if isinstance(lt, float):
        lt_str = str(int(lt)) if lt.is_integer() else str(lt)
    else:
        s = str(lt)
        lt_str = s[:-2] if s.endswith(".0") else s

    return f"{eid}_{lt_str}"


def _enrich_new_process_name(event, eid):
    #enrich a process with the process name 
    npn = event.get("EventData.NewProcessName")
    if npn is None or _is_nan_value(npn):
        return None

    s = str(npn)
    proc = s.replace("/", "\\").split("\\")[-1]
    proc = os.path.splitext(proc)[0]
    return f"{eid}_{proc}"


def _enrich_4657(event, eid):
    #enrichinh specific types of 4657 events 
    val = (
        event.get("EventData.ObjectValueName")
        or event.get("EventData.ValueName")
        or event.get("EventData.OperationType")
        or event.get("EventData.Type")
    )
    if val is None or _is_nan_value(val):
        return None

    if "common" in str(val).strip().lower():
        return f"{eid}_common"

    return None


# Mapping of base EventID -> enrichment function that can produce a more specific `concept:name`.
ENRICHMENT_HANDLERS = {
    "4624": _enrich_logon_type,
    "4634": _enrich_logon_type,
    "4688": _enrich_new_process_name,
    "4657": _enrich_4657,
}


def enrich_event_ids(event_log):
    new_log = EventLog(attributes=event_log.attributes)

    for trace in event_log:
        logonid_to_lt = {}

        # Collect LogonType by logon ID from 4624 events.
        for event in trace:
            raw_eid = event.get("EventID", event.get("concept:name"))
            if raw_eid is None:
                continue

            eid = str(raw_eid)
            base_eid = eid.split("_", 1)[0]
            if base_eid != "4624":
                continue

            lt_str = _format_logon_type_value(event.get("EventData.LogonType"))
            if lt_str is None:
                continue

            subj = _normalize_logon_id(event.get("EventData.SubjectLogonId"))
            targ = _normalize_logon_id(event.get("EventData.TargetLogonId"))

            if subj:
                logonid_to_lt[subj] = lt_str
            if targ:
                logonid_to_lt[targ] = lt_str

        # Apply enrichments and special-case 4672.
        for event in trace:
            raw_eid = event.get("EventID", event.get("concept:name"))
            if raw_eid is None:
                continue

            eid = str(raw_eid)
            base_eid = eid.split("_", 1)[0]

            handler = ENRICHMENT_HANDLERS.get(eid)
            if handler is None and "_" in eid:
                handler = ENRICHMENT_HANDLERS.get(base_eid)

            if handler is not None:
                handler_eid = eid if ENRICHMENT_HANDLERS.get(eid) is not None else base_eid
                new_name = handler(event, handler_eid)
                if new_name:
                    event["concept:name"] = str(new_name)

            if base_eid == "4672":
                id4672 = _normalize_logon_id(
                    event.get("EventData.TargetLogonId")
                    or event.get("EventData.SubjectLogonId")
                )
                if id4672:
                    lt_str = logonid_to_lt.get(id4672)
                    if lt_str is not None:
                        event["concept:name"] = f"4672_{lt_str}"

        # Merge certain 4690+4658 adjacent pairs and drop unmerged 4690s.
        events = list(trace)
        merged_events = []
        i = 0

        while i < len(events):
            if i < len(events) - 1:
                ev1 = events[i]
                ev2 = events[i + 1]

                eid1 = str(ev1.get("EventID", ev1.get("concept:name", ""))).split("_", 1)[0]
                eid2 = str(ev2.get("EventID", ev2.get("concept:name", ""))).split("_", 1)[0]

                if eid1 == "4690" and eid2 == "4658":
                    h1 = _normalize_handle(
                        ev1.get("EventData.TargetHandleId") or ev1.get("EventData.TargetHandleID")
                    )
                    h2 = _normalize_handle(
                        ev2.get("EventData.HandleId") or ev2.get("EventData.HandleID")
                    )

                    if h1 and h2 and h1 == h2:
                        ev1["concept:name"] = "4690_4658"
                        merged_events.append(ev1)
                        i += 2
                        continue

            cur = events[i]
            cur_eid = str(cur.get("EventID", cur.get("concept:name", ""))).split("_", 1)[0]
            cur_name = str(cur.get("concept:name", ""))

            # Drop standalone 4690 events unless they were merged into 4690_4658.
            if cur_eid == "4690" and cur_name != "4690_4658":
                i += 1
                continue

            merged_events.append(cur)
            i += 1

        new_log.append(Trace(merged_events, attributes=trace.attributes))

    return new_log


def filter_events(event_log, config):
    new_log = EventLog(attributes=event_log.attributes)

    # Keeping only allowed events
    allowed_4688 = config.allowed_4688

    # For certain events we dont want duplicates in a row 
    dedup_names = {config.trace_start_prefix, config.trace_end_prefix}

    for trace in event_log:
        new_events = []
        last_kept_name = None

        for ev in trace:
            eid = get_eid(ev)
            cname = str(ev.get("concept:name", ""))

            if eid.startswith("4688"):
                if cname not in allowed_4688:
                    continue

            if cname in dedup_names and cname == last_kept_name:
                continue

            new_events.append(ev)
            last_kept_name = cname

        if new_events:
            new_log.append(Trace(new_events, attributes=trace.attributes))

    return new_log


def drop_leading(event_log):
    # We see a very specific start pattern for some traces that are normalized
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
        if remaining:
            new_log.append(Trace(remaining, attributes=trace.attributes))

    return new_log


def drop_trailing(event_log):
    # We see a very specific end pattern for some traces that are normalized
    new_log = EventLog(attributes=event_log.attributes)

    for trace in event_log:
        events = list(trace)
        if not events:
            continue

        end_idx = len(events)

        if end_idx > 0 and get_eid(events[end_idx - 1]).startswith("4658"):
            end_idx -= 1

        if end_idx > 0 and get_eid(events[end_idx - 1]).startswith("4690"):
            cname = str(events[end_idx - 1].get("concept:name", ""))
            if cname != "4690_4658":
                end_idx -= 1

        remaining = events[:end_idx]
        if remaining:
            new_log.append(Trace(remaining, attributes=trace.attributes))

    return new_log


def filter_traces(event_log, config):
    new_log = EventLog(attributes=event_log.attributes)

    for trace in event_log:
        events = list(trace)
        if not events:
            continue

        # keep the first of 4624_2 or 4625
        start_idx = None
        for idx, ev in enumerate(events):
            cname = str(ev.get("concept:name", ""))
            base = get_eid(ev).split("_", 1)[0]
            if cname.startswith(config.trace_start_prefix) or base == "4625":
                start_idx = idx
                break

        # Find first 4634_2
        end_idx = None
        for j, ev in enumerate(events):
            cname = str(ev.get("concept:name", ""))
            if cname.startswith(config.trace_end_prefix):
                end_idx = j
                break

        if start_idx is None or end_idx is None or start_idx > end_idx:
            continue

        trimmed_events = events[start_idx : end_idx + 1]
        if trimmed_events:
            new_log.append(Trace(trimmed_events, attributes=trace.attributes))

    return new_log


def csv_to_xes(csv_path, xes_out, windows, config: LogConfig = LogConfig()):
    # converting a csv file into an xes file 
    df = pd.read_csv(csv_path)

    if config.timestamp_col not in df.columns:
        raise ValueError(f"Timestamp column '{config.timestamp_col}' not in CSV.")

    df = df.copy()
    df["time:timestamp"] = (
        pd.to_datetime(df[config.timestamp_col], errors="coerce", utc=True).dt.tz_convert(None)
    )
    df = df.dropna(subset=["time:timestamp"])

    pieces = []
    for i, (start, end) in enumerate(windows, start=1):
        start_ts = pd.to_datetime(start, utc=True).tz_convert(None)
        end_ts = pd.to_datetime(end, utc=True).tz_convert(None)

        mask = (df["time:timestamp"] > start_ts) & (df["time:timestamp"] < end_ts)
        sub = df.loc[mask].copy()
        if sub.empty:
            continue

        sub["case:concept:name"] = f"trace_{i}"
        sub["concept:name"] = sub[config.eventid_col].astype(str)
        pieces.append(sub)

    if not pieces:
        raise ValueError("No events fell into any of the given time windows.")

    df_traces = pd.concat(pieces, ignore_index=True)
    df_traces["case:concept:name"] = df_traces["case:concept:name"].astype(str)
    df_traces["concept:name"] = df_traces["concept:name"].astype(str)

    event_log = log_converter.apply(df_traces, variant=log_converter.Variants.TO_EVENT_LOG)

    # Clean NaN-like values from PM4Py structures to avoid invalid XES attributes.
    for trace in event_log:
        for k in [k for k, v in trace.attributes.items() if _is_nan_value(v)]:
            del trace.attributes[k]
        for event in trace:
            for k in [k for k, v in event.items() if _is_nan_value(v)]:
                del event[k]

    event_log = enrich_event_ids(event_log)
    event_log = filter_events(event_log, config)
    event_log = drop_leading(event_log)
    event_log = drop_trailing(event_log)
    event_log = filter_traces(event_log, config)

    pm4py.write_xes(event_log, xes_out)


def keep_last_trace(xes):
    # Xes util method that cuts everything but the last trace from an xes 
    xes_path = Path(xes)

    tree = ET.parse(xes_path)
    root = tree.getroot()

    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}", 1)[0][1:]
        ET.register_namespace("", ns)

    def q(tag: str) -> str:
        return f"{{{ns}}}{tag}" if ns else tag

    traces = [child for child in list(root) if child.tag == q("trace")]
    if not traces:
        raise ValueError("No <trace> elements found in this XES file.")

    first_trace = traces[0]
    last_trace = traces[-1]

    first_name = None
    for child in list(first_trace):
        if child.tag == q("string") and child.attrib.get("key") == "concept:name":
            first_name = child.attrib.get("value")
            break

    for tr in traces:
        root.remove(tr)

    if first_name is not None:
        name_elem = None
        for child in list(last_trace):
            if child.tag == q("string") and child.attrib.get("key") == "concept:name":
                name_elem = child
                break
        if name_elem is None:
            last_trace.insert(0, ET.Element(q("string"), {"key": "concept:name", "value": first_name}))
        else:
            name_elem.set("value", first_name)

    root.append(last_trace)

    with tempfile.NamedTemporaryFile("wb", delete=False, dir=str(xes_path.parent), suffix=".xes") as tmp:
        tmp_path = Path(tmp.name)
        tree.write(tmp, encoding="utf-8", xml_declaration=True)
    os.replace(tmp_path, xes_path)
