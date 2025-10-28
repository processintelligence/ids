import json
import os
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.objects.petri_net.obj import PetriNet, Marking
from PetriNetUtil.IPetriNetUtil import IPetriNetUtil
import xml.etree.ElementTree as ET
import shutil
import re

class PetriNetUtil(IPetriNetUtil):
    def __init__(self):
        pass

    def get_petrinet(self, pnml_path):

        net, initial_marking, final_marking = pnml_importer.apply(pnml_path)

        net.name = os.path.splitext(os.path.basename(pnml_path))[0]

        return net, initial_marking, final_marking

    def create_blanc_config(self, petrinet, output_path, save_to_disk):
        place_transition_arc = {}

        for arc in petrinet.arcs:
            src = arc.source
            tgt = arc.target

            # we only care about arcs Place -> Transition
            is_place_to_trans = (
                hasattr(src, "in_arcs") and hasattr(src, "out_arcs") and
                hasattr(tgt, "in_arcs") and hasattr(tgt, "out_arcs") and
                (src in petrinet.places) and (tgt in petrinet.transitions)
            )
            if not is_place_to_trans:
                continue

            place_id = src.name
            trans_id = tgt.name

            if place_id not in place_transition_arc:
                place_transition_arc[place_id] = {}

            arc_key = f"{place_id}_{trans_id}"

            place_transition_arc[place_id][arc_key] = ""

        config = {
            "pnmlfilename": os.path.basename(petrinet.name),
            "behavior": "",
            "place_transition_arc": place_transition_arc
        }

        if save_to_disk:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

        return config
    
    def validate_config(self, config):
        with open(config, "r", encoding="utf-8") as f:
            config_json = json.load(f)

        arcs = config_json.get("place_transition_arc", {})
        all_valid = True

        for place, transitions in arcs.items():
            try:
                values = [float(v) for v in transitions.values() if str(v).strip() != ""]
            except ValueError:
                print(f"Non-numeric value in {place}: {transitions}")
                all_valid = False
                continue

            total = sum(values)
            if abs(total - 1.0) > 1e-6:
                print(f"{place}: Sum = {total:.3f} (should equal 1.0)")
                all_valid = False

        return all_valid
    
    def obtain_guards(self, petrinet, config):
        with open(config, "r", encoding="utf-8") as f:
            config_json = json.load(f)
        config_arcs = config_json.get("place_transition_arc", {})

        pre_conditions = {}
        post_conditions = {}

        #finding preconditions
        for p in petrinet.places:
            prob_sum = 0
            for arc in p.out_arcs:
                transition = arc.target.name
                place = arc.source
                config_key = f"{place}_{transition}"


                prob = float(config_arcs[str(p)][config_key])

                if prob_sum == 0:
                    pre_conditions[transition] = f"{p} <= {prob}"
                    prob_sum = prob_sum + prob
                else:
                    pre_conditions[transition] = f"{p} > {prob_sum} && {p} <= {prob_sum + prob}"
                    prob_sum = prob_sum + prob

        #finding postconditions
        for p in petrinet.places:
            for arc in p.in_arcs:
                transition = arc.source.name

                post_conditions[transition] = f"{p}' > 0"                    
                    
        return pre_conditions, post_conditions

    def combine_guards(self, pre_conditions, post_conditions):
        combined_guards = {}

        all_transitions = set(pre_conditions.keys()) | set(post_conditions.keys())
        
        for t in all_transitions:
                pre = pre_conditions.get(t)
                post = post_conditions.get(t)

                if pre and post:
                    combined_guards[t] = f"(({pre})&&({post}))"
                elif pre:
                    combined_guards[t] = pre
                elif post:
                    combined_guards[t] = post

        return combined_guards
    
    def create_data_pnml(self, guards, pnml_path, config_path):
        folder = os.path.dirname(pnml_path)
        filename = os.path.basename(pnml_path)
        data_filename = f"data_{filename}"
        data_pnml_path = os.path.join(folder, data_filename)
        shutil.copyfile(pnml_path, data_pnml_path)

        self._inject_variables(config_path, data_pnml_path)

        self._inject_guards(guards, data_pnml_path)

        self._inject_write_varibales(data_pnml_path)

        return data_pnml_path

    def _inject_variables(self, config_path, pnml_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config_json = json.load(f)

        config_arcs = config_json.get("place_transition_arc", {})
        place_names = list(config_arcs.keys())

        tree = ET.parse(pnml_path)
        root = tree.getroot()

        if root.tag.startswith("{"):
            ns_uri = root.tag.split("}", 1)[0][1:]
            nsmap = {"pnml": ns_uri}

            def q(tag: str) -> str:
                return f"{{{ns_uri}}}{tag}"

            net_el = root.find("pnml:net", nsmap)
            if net_el is None:
                raise RuntimeError("Could not find <net> element in PNML (namespaced).")

            variables_el = ET.Element(q("variables"))

            for place_name in place_names:
                var_el = ET.SubElement(
                    variables_el,
                    q("variable"),
                    {
                        "maxValue": "100000.0",
                        "minValue": "0.0",
                        "type": "java.lang.Double"
                    }
                )
                name_el = ET.SubElement(var_el, q("name"))
                name_el.text = place_name

            net_el.append(variables_el)

            ET.register_namespace("", ns_uri)

        else:
            def q(tag: str) -> str:
                return tag

            net_el = root.find("net")
            if net_el is None:
                raise RuntimeError("Could not find <net> element in PNML (no namespace).")

            variables_el = ET.Element("variables")

            for place_name in place_names:
                var_el = ET.SubElement(
                    variables_el,
                    "variable",
                    {
                        "maxValue": "100000.0",
                        "minValue": "0.0",
                        "type": "java.lang.Double"
                    }
                )
                name_el = ET.SubElement(var_el, "name")
                name_el.text = place_name

            net_el.append(variables_el)

        tree.write(pnml_path, encoding="utf-8", xml_declaration=True)

    def _inject_guards(self, guards, pnml_path):
        tree = ET.parse(pnml_path)
        root = tree.getroot()

        if root.tag.startswith("{"):
            ns_uri = root.tag.split("}", 1)[0][1:]
            nsmap = {"pnml": ns_uri}

            def q(tag: str) -> str:
                return f"{{{ns_uri}}}{tag}"

            transition_elems = root.findall(".//pnml:transition", nsmap)

            ET.register_namespace("", ns_uri)

        else:
            def q(tag: str) -> str:
                return tag

            transition_elems = root.findall(".//transition")

        for t_el in transition_elems:
            t_id = t_el.get("id")
            if not t_id:
                continue 

            if t_id in guards:
                raw_guard = guards[t_id]

                t_el.set("guard", raw_guard)

        tree.write(pnml_path, encoding="utf-8", xml_declaration=True)

    def _inject_write_varibales(self, pnml_path: str) -> None:
        tree = ET.parse(pnml_path)
        root = tree.getroot()

        if root.tag.startswith("{"):
            ns_uri = root.tag.split("}", 1)[0][1:]
            nsmap = {"pnml": ns_uri}

            def q(tag: str) -> str:
                return f"{{{ns_uri}}}{tag}"

            transition_elems = root.findall(".//pnml:transition", nsmap)

            ET.register_namespace("", ns_uri)
        else:
            def q(tag: str) -> str:
                return tag

            transition_elems = root.findall(".//transition")

        prime_pattern = re.compile(r"([A-Za-z_]\w*)'")

        for t_el in transition_elems:
            guard_expr = t_el.get("guard")
            if not guard_expr:
                continue

            written_vars = set(prime_pattern.findall(guard_expr))

            if not written_vars:
                continue

            existing_vars = set()
            for child in list(t_el):
                if child.tag == q("writeVariable"):
                    if child.text is not None:
                        existing_vars.add(child.text.strip())

            for var in written_vars:
                if var not in existing_vars:
                    wv_el = ET.SubElement(t_el, q("writeVariable"))
                    wv_el.text = var

        tree.write(pnml_path, encoding="utf-8", xml_declaration=True)

# -----------------------------------
if __name__ == "__main__":
    # Input PNML and output config
    pnml_file = "PNMLFiles/simplest_ex.pnml"
    config_path = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/Configs/config1.json"
    config_path1 = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/Configs/config2.json"

    util = PetriNetUtil()

    # 1. Load Petri net from PNML
    net, im, fm = util.get_petrinet(pnml_file)
    print("Petri net loaded successfully!")
    print(f"Net name: {net.name}")
    print("Places:", [p.name for p in net.places])
    print("Transitions:", [t.name for t in net.transitions])
    print("Initial marking:", {p.name: t for p, t in im.items()})

    # 2. Create blank config JSON in the new nested structure
    config = util.create_blanc_config(net, config_path, True)
    print("\nGenerated blank config:")
    print(json.dumps(config, indent=4))

    # 3. Validate that config
    is_valid = util.validate_config(config_path1)
    print("Overall valid?", is_valid)

    # 4. inject guards into pnml
    pre, post = util.obtain_guards(net, config_path1)

    print("pre:", pre)
    print("post:", post)

    # 5. combine the guards
    combined = util.combine_guards(pre, post)
    print("combined", combined)

    #6. inject the obtain guards into the pnml
    data_pnml_path = util.create_data_pnml(combined, pnml_file, config_path1)
