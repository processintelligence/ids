import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import math
import numpy as np
import copy
from datetime import datetime

def generate_naive_df_time(xes_path):
    # dict[A][B] = list of time differences between A and B
    time_diffs = defaultdict(lambda: defaultdict(list))

    tree = ET.parse(xes_path)
    root = tree.getroot()

    ns = {'xes': 'http://www.xes-standard.org/'}

    for trace in root.findall('xes:trace', ns):
        events = []

        for event in trace.findall('xes:event', ns):
            name_attr = event.find("xes:string[@key='concept:name']", ns)
            time_attr = event.find("xes:date[@key='time:timestamp']", ns)

            if name_attr is None or time_attr is None:
                continue

            # parse time
            timestamp = datetime.fromisoformat(time_attr.get("value"))

            events.append((name_attr.get("value"), timestamp))

        # Build time difference list
        for i in range(len(events) - 1):
            e1, t1 = events[i]
            e2, t2 = events[i + 1]

            diff_seconds = (t2 - t1).total_seconds()

            time_diffs[e1][e2].append(diff_seconds)

    return time_diffs

def generate_translated_df_time(xes_path):
    # dict[A][B] = list of time differences between A and B
    time_diffs = defaultdict(lambda: defaultdict(list))

    tree = ET.parse(xes_path)
    root = tree.getroot()

    ns = {'xes': 'http://www.xes-standard.org/'}

    for trace in root.findall('xes:trace', ns):
        events = []

        for event in trace.findall('xes:event', ns):
            name_attr = event.find("xes:string[@key='concept:name']", ns)
            time_attr = event.find("xes:date[@key='time:timestamp']", ns)

            if name_attr is None or time_attr is None:
                continue

            # parse time
            timestamp = datetime.fromisoformat(time_attr.get("value"))

            #if the event is 'init_t', dont add it
            if name_attr.get('value').startswith('init_t'):
                continue
            #if the event is '4608', dont add it
            if name_attr.get('value').startswith('4608'):
                continue
            #if the event is '4609', dont add it
            if name_attr.get('value').startswith('4609'):
                continue
            #if the event is '1100', dont add it
            if name_attr.get('value').startswith('1100'):
                continue
            #if name starts with 'tau', dont add it
            if name_attr.get('value').startswith('tau'):
                continue
            #if name starts with '4688', add it as '4688' except if it is 'conhost' or 'cmd'. Also safe is exe is part of the name
            if name_attr.get('value').startswith('4688') and (name_attr.get('value').endswith('_cmd') or name_attr.get('value').endswith('_conhost') or name_attr.get('value').endswith('_cmd.exe') or name_attr.get('value').endswith('_conhost.exe')):
                cleaned_value = name_attr.get('value').replace('.exe', '')
                events.append((cleaned_value, timestamp))
                continue
            elif name_attr.get('value').startswith('4688'):
                events.append(('4688', timestamp))
                continue
            #if name starts with '4672', add it as '4672'
            if name_attr.get('value').startswith('4672'):
                events.append(('4672', timestamp))
                continue
            #if name starts with '4625', dont add it
            if name_attr.get('value').startswith('4625'):
                continue
            #if name starts with '4634', add it as '4634' and does not contain _3, _4, _5, but if its _10, _11 we dont want to keep it at all
            if name_attr.get('value').startswith('4634') and (name_attr.get('value').endswith('_10') or name_attr.get('value').endswith('_1')):
                continue
            if name_attr.get('value').startswith('4634') and (name_attr.get('value').endswith('_3') or name_attr.get('value').endswith('_4') or name_attr.get('value').endswith('_5')):
                events.append((name_attr.get('value'), timestamp)) 
                continue
            elif name_attr.get('value').startswith('4634'):
                events.append(('4634', timestamp))
                continue
            #if name starts with '4656', add it as '4688'
            if name_attr.get('value').startswith('4656'):
                events.append(('4688', timestamp))
                continue
            #if the event is '4663', dont add it
            if name_attr.get('value').startswith('4663'):
                continue
            #if the event is '4657', dont add it
            if name_attr.get('value').startswith('4657'):
                continue
            #if the event is '4658', dont add it
            if name_attr.get('value').startswith('4658'):
                continue
            #if the event is '4624_10', dont add it
            if name_attr.get('value').startswith('4624_10'):
                continue
            #if the event is '4624_11', dont add it
            if name_attr.get('value').startswith('4624_11'):
                continue
            #if the event is '4803', dont add it
            if name_attr.get('value').startswith('4803'):
                continue
            #if the event is '4802', dont add it
            if name_attr.get('value').startswith('4802'):
                continue
            #if the event is '4647', dont add it
            if name_attr.get('value').startswith('4647'):
                continue
            #else add the event unchanged
            events.append((name_attr.get('value'), timestamp))

        # Build time difference list
        for i in range(len(events) - 1):
            e1, t1 = events[i]
            e2, t2 = events[i + 1]

            diff_seconds = (t2 - t1).total_seconds()

            time_diffs[e1][e2].append(diff_seconds)

    return time_diffs

import numpy as np

def compute_df_stats(df_dict):
    stats = {}

    for a, followers in df_dict.items():
        stats[a] = {}
        for b, durations in followers.items():
            arr = np.array(durations, dtype=float)

            if arr.size == 0:
                stats[a][b] = {
                    "count": 0,
                    "mean": None,
                    "median": None,
                    "std": None,
                    "min": None,
                    "max": None,
                    "sum": None,
                }
            else:
                stats[a][b] = {
                    "count": int(arr.size),
                    "mean": float(np.mean(arr)),
                    "median": float(np.median(arr)),
                    "std": float(np.std(arr)),
                    "min": float(np.min(arr)),
                    "max": float(np.max(arr)),
                    "sum": float(np.sum(arr)),
                }

    return stats




xes_path_R = r"c:\Users\lomo0\Documents\RandomScripts\wls_800MB.xes"
df_time_R = generate_translated_df_time(xes_path_R)

df_stats = compute_df_stats(df_time_R)

print(df_stats)
