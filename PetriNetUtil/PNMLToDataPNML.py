import json
import os
import copy
import re
import xml.etree.ElementTree as ET

from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils

from PetriNetUtil.IPNMLToDataPNML import IPNMLToDataPNML


class PNMLToDataPNML(IPNMLToDataPNML):
    def __init__(self, pnml_path: str, config_dir: str):
        self.pnml_path = pnml_path
        self.data_pnml_out_dir = "GeneratedFiles/DataPNML"
        self.config_dir = config_dir

    # PUBLIC API
    def generate_config_structure(self) -> str:
        net, im, fm = self._get_petrinet(self.pnml_path)

        new_net, new_im, new_fm = self._add_init_place(net, im, fm)

        self._create_pnml(new_net, new_im, new_fm, self.data_pnml_out_dir)

        config_path = self._create_blanc_config(net)

        return config_path

    def generate_data_petrinet(self) -> str:
        base_name = os.path.splitext(os.path.basename(self.pnml_path))[0]
        config_path = os.path.join(self.config_dir, f"{base_name}_config.json")

        is_valid = self._validate_config(config_path)

        if not is_valid:
            raise ValueError("Config is not valid: probabilities per place must sum to 1.0")

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        pnml_filename = cfg.get("pnmlfilename")
        if not pnml_filename:
            raise ValueError("Config is missing 'pnmlfilename'")

        base_name = os.path.splitext(pnml_filename)[0]
        wrapped_name = f"data_{base_name}.pnml"
        wrapped_path = os.path.join(self.data_pnml_out_dir, wrapped_name)

        if os.path.exists(wrapped_path):
            pnml_path_to_use = wrapped_path
        else:
            cfg_dir = os.path.dirname(config_path)
            pnml_path_to_use = os.path.join(cfg_dir, pnml_filename)

        petrinet, im, fm = self._get_petrinet(pnml_path_to_use)

        pre_conditions, post_conditions = self._obtain_guards(petrinet, config_path)
        combined_guards = self._combine_guards(pre_conditions, post_conditions)

        data_pnml_path = self._create_data_pnml(combined_guards, pnml_path_to_use, config_path)

        return data_pnml_path

    # PRIVATE METHODS
    def _get_petrinet(self, pnml_path: str):
        net, initial_marking, final_marking = pnml_importer.apply(pnml_path)
        net.name = os.path.splitext(os.path.basename(pnml_path))[0]
        return net, initial_marking, final_marking

    def _add_init_place(self, petrinet: PetriNet, im: Marking, fm: Marking):
        if not im:
            raise ValueError("Petri net has to have an initial marking.")

        originally_marked_place_names = [p.name for p in im.keys()]

        if "init_p" in [p.name for p in petrinet.places]:
            raise ValueError("You can not have a place called init_p.")
        if "init_t" in [t.name for t in petrinet.transitions]:
            raise ValueError("You can not have a transition called init_t")

        new_net = copy.deepcopy(petrinet)
        new_im = Marking()
        new_fm = copy.deepcopy(fm)

        places_by_name = {p.name: p for p in new_net.places}

        init_place = PetriNet.Place("init_p")
        new_net.places.add(init_place)

        init_transition = PetriNet.Transition("init_t", "init_t")
        new_net.transitions.add(init_transition)

        # init_p -> init_t
        petri_utils.add_arc_from_to(init_place, init_transition, new_net)

        # init_t -> originally marked places
        for place_name in originally_marked_place_names:
            target_place = places_by_name[place_name]
            already_connected = any(
                arc.source is init_transition and arc.target is target_place
                for arc in new_net.arcs
            )
            if not already_connected:
                petri_utils.add_arc_from_to(init_transition, target_place, new_net)

        # new initial marking
        new_im[init_place] = 1

        return new_net, new_im, new_fm

    def _create_pnml(self, petri_net, im, fm, output_folder: str) -> str:
        os.makedirs(output_folder, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(petri_net.name))[0]
        filename = f"data_{base_name}.pnml"
        data_pnml_path = os.path.join(output_folder, filename)
        pnml_exporter.apply(petri_net, im, data_pnml_path, final_marking=fm)
        return data_pnml_path

    def _create_blanc_config(self, petrinet) -> str:
        os.makedirs(self.config_dir, exist_ok=True)

        # name based on the original pnml we were constructed with
        base_name = os.path.splitext(os.path.basename(self.pnml_path))[0]
        config_path = os.path.join(self.config_dir, f"{base_name}_config.json")

        place_transition_arc = {}

        for arc in petrinet.arcs:
            src = arc.source
            tgt = arc.target

            if (src in petrinet.places) and (tgt in petrinet.transitions):
                place_id = src.name
                trans_id = tgt.name

                if place_id not in place_transition_arc:
                    place_transition_arc[place_id] = {}

                arc_key = f"{place_id}_{trans_id}"
                place_transition_arc[place_id][arc_key] = ""

        places = [place.name for place in petrinet.places]

        config = {
            "pnmlfilename": os.path.basename(petrinet.name),
            "behavior": "",
            "places": places,
            "place_transition_arc": place_transition_arc,
        }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        return config_path

    def _validate_config(self, config_path):
        with open(config_path, "r", encoding="utf-8") as f:
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

    def _obtain_guards(self, petrinet, config_path: str):
        with open(config_path, "r", encoding="utf-8") as f:
            config_json = json.load(f)

        config_arcs = config_json.get("place_transition_arc", {})

        pre_conditions = self._build_pre_conditions(petrinet, config_arcs)
        post_conditions = self._build_post_conditions(petrinet)

        return pre_conditions, post_conditions

    def _build_pre_conditions(self, petrinet, config_arcs: dict):
        pre_conditions = {}

        for place in petrinet.places:
            p_name = place.name

            if p_name not in config_arcs:
                continue

            prob_sum = 0.0
            for arc in place.out_arcs:
                transition_name = arc.target.name
                config_key = f"{p_name}_{transition_name}"

                if config_key not in config_arcs[p_name]:
                    continue

                prob = float(config_arcs[p_name][config_key])

                if prob_sum == 0.0:
                    pre_conditions[transition_name] = f"{p_name} <= {prob}"
                else:
                    pre_conditions[transition_name] = (
                        f"{p_name} > {prob_sum} && {p_name} <= {prob_sum + prob}"
                    )

                prob_sum += prob

        return pre_conditions

    def _build_post_conditions(self, petrinet):
        post_conditions = {}
        for place in petrinet.places:
            p_name = place.name
            for arc in place.in_arcs:
                transition_name = arc.source.name
                post_conditions[transition_name] = f"{p_name}' > 0"
        return post_conditions

    def _combine_guards(self, pre_conditions, post_conditions):
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

    def _create_data_pnml(self, guards, data_pnml_path: str, config_path: str):
        self._inject_variables(config_path, data_pnml_path)
        self._inject_guards(guards, data_pnml_path)
        self._inject_write_varibales(data_pnml_path)
        return data_pnml_path

    # ---------- XML injection helpers ----------
    def _inject_variables(self, config_path, pnml_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config_json = json.load(f)

        place_names = config_json.get("places", [])

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
                        "type": "java.lang.Double",
                    },
                )
                name_el = ET.SubElement(var_el, q("name"))
                name_el.text = place_name

            net_el.append(variables_el)

            ET.register_namespace("", ns_uri)

        else:
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
                        "type": "java.lang.Double",
                    },
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

    def _inject_write_varibales(self, pnml_path):
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
                if child.tag == q("writeVariable") and child.text is not None:
                    existing_vars.add(child.text.strip())

            for var in written_vars:
                if var not in existing_vars:
                    wv_el = ET.SubElement(t_el, q("writeVariable"))
                    wv_el.text = var

        tree.write(pnml_path, encoding="utf-8", xml_declaration=True)

"""
# -----------------------------------
if __name__ == "__main__":
    pnml_file = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/PNMLFiles/simplest_ex.pnml"
    pnml_output_dir = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/PNMLFiles"
    config_output_dir = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/Configs"

    util = PetriNetUtil(
        pnml_path=pnml_file,
        data_pnml_out_dir=pnml_output_dir,
        config_out_dir=config_output_dir,
    )

    #cfg = util.generate_config_structure()
    #print("config:", cfg)

    path = "/Users/emilpontoppidanrasmussen/Dropbox/Dtu/Kandidat/4_semester/Masters/Master Repo/MasterRepo/Configs/simplest_ex_config.json"
    data_pnml = util.generate_data_petrinet()
    print("data pnml:", data_pnml)
"""