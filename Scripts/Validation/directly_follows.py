import xml.etree.ElementTree as ET
from collections import defaultdict
import os

def generate_naive_directly_follows(xes_path):
    directly_follows = defaultdict(lambda: defaultdict(int))

    tree = ET.parse(xes_path) 
    root = tree.getroot()

    ns = {'xes': 'http://www.xes-standard.org/'}

    for trace in root.findall('xes:trace', ns):
        events = []
        for event in trace.findall('xes:event', ns):
            name_attr = event.find("xes:string[@key='concept:name']", ns)
            if name_attr is not None:
                events.append(name_attr.get('value'))

        for i in range(len(events) - 1):
            e1 = events[i]
            e2 = events[i + 1]
            directly_follows[e1][e2] += 1

    return directly_follows

def generate_translated_directly_follows(xes_path):
    directly_follows = defaultdict(lambda: defaultdict(int))

    tree = ET.parse(xes_path) 
    root = tree.getroot()

    ns = {'xes': 'http://www.xes-standard.org/'}

    for trace in root.findall('xes:trace', ns):
        events = []
        for event in trace.findall('xes:event', ns):
            name_attr = event.find("xes:string[@key='concept:name']", ns)
            
            if name_attr is not None:
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
                    events.append(cleaned_value)
                    continue
                elif name_attr.get('value').startswith('4688'):
                    events.append('4688')
                    continue
                #if name starts with '4625', dont add it
                if name_attr.get('value').startswith('4625'):
                    continue
                #if name starts with '4634', add it as '4634' and does not contain _3, _4, _5, but if its _10, _11 we dont want to keep it at all
                if name_attr.get('value').startswith('4634') and (name_attr.get('value').endswith('_10') or name_attr.get('value').endswith('_1')):
                    continue
                if name_attr.get('value').startswith('4634') and (name_attr.get('value').endswith('_3') or name_attr.get('value').endswith('_4') or name_attr.get('value').endswith('_5')):
                    events.append(name_attr.get('value')) 
                    continue
                elif name_attr.get('value').startswith('4634'):
                    events.append('4634')
                    continue
                #if name starts with '4656', add it as '4688'
                if name_attr.get('value').startswith('4656'):
                    events.append('4688')
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
                events.append(name_attr.get('value'))

        for i in range(len(events) - 1):
            e1 = events[i]
            e2 = events[i + 1]
            directly_follows[e1][e2] += 1

    return directly_follows

def normalize_directly_follows(directly_follows_dict):
    pass

""" base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, '..', '..', 'GeneratedFiles', 'WebPPL_XES', 'data_phase_1_net.xes')
xes_file_path  = os.path.abspath(file_path) """

xes_file_path = r"c:\Users\lomo0\Documents\RandomScripts\wls_800MB.xes"

df_matrix = generate_translated_directly_follows(xes_file_path)
for e1, next_events in df_matrix.items():
    print(e1)