#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def strip_namespace(tag: str) -> str:
    """Return the local tag name without XML namespace."""
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def fix_transition_ids_inplace(pnml_path: str) -> None:
    """
    Load a PNML file, set each transition's id to its <name><text> value,
    and update all source/target references accordingly. Overwrites the file.
    """
    pnml_file = Path(pnml_path)
    if not pnml_file.exists():
        raise FileNotFoundError(f"File not found: {pnml_path}")

    tree = ET.parse(pnml_file)
    root = tree.getroot()

    id_map = {}  # old_id -> new_id

    # 1) Update transition ids based on <name><text>
    for t in root.iter():
        if strip_namespace(t.tag) != "transition":
            continue

        # Find <name> child
        name_el = None
        for child in t:
            if strip_namespace(child.tag) == "name":
                name_el = child
                break
        if name_el is None:
            continue

        # Find <text> inside <name>
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

    # 2) Update arc references (source/target) using the id_map
    if id_map:
        for elem in root.iter():
            for attr in ("source", "target"):
                val = elem.get(attr)
                if val in id_map:
                    elem.set(attr, id_map[val])

    # 3) Overwrite the original file
    tree.write(pnml_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    pnml_path = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/PNMLFiles/phase_2_net.pnml"
    
    fix_transition_ids_inplace(pnml_path)

    print("done")