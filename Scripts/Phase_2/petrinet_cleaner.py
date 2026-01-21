#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def strip_namespace(tag):
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def fix_transition_ids_inplace(pnml_path):
    pnml_file = Path(pnml_path)
    if not pnml_file.exists():
        raise FileNotFoundError(f"File not found: {pnml_path}")

    tree = ET.parse(pnml_file)
    root = tree.getroot()

    id_map = {}  # old_id -> new_id

    for t in root.iter():
        if strip_namespace(t.tag) != "transition":
            continue

        name_el = None
        for child in t:
            if strip_namespace(child.tag) == "name":
                name_el = child
                break
        if name_el is None:
            continue

        text_el = None
        for child in name_el:
            if strip_namespace(child.tag) == "text":
                text_el = child
                break
        if text_el is None or text_el.text is None:
            continue

        new_id = text_el.text.strip()
        if not new_id:
            continue

        old_id = t.get("id")
        if old_id and old_id != new_id:
            id_map[old_id] = new_id
            t.set("id", new_id)

    if id_map:
        for elem in root.iter():
            for attr in ("source", "target"):
                val = elem.get(attr)
                if val in id_map:
                    elem.set(attr, id_map[val])

    tree.write(pnml_file, encoding="utf-8", xml_declaration=True)
