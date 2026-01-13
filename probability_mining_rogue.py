import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from collections import defaultdict
from typing import Dict, Tuple, Any
import json

def marking_to_key(marking):
    return tuple(sorted((p.name, marking[p]) for p in marking if marking[p] > 0))


def is_enabled(marking, transition):
    for arc in transition.in_arcs:
        p = arc.source
        if marking.get(p, 0) <= 0:
            return False
    return True


def fire_transition(marking, transition):
    new_marking = marking.copy()

    # consume
    for arc in transition.in_arcs:
        p = arc.source
        new_marking[p] = new_marking.get(p, 0) - 1
        if new_marking[p] <= 0:
            new_marking.pop(p, None)

    # produce
    for arc in transition.out_arcs:
        p = arc.target
        new_marking[p] = new_marking.get(p, 0) + 1

    return new_marking


def transition_id(t):
    return t.label if t.label is not None else f"{t.name}"


def preset_place_names(t):
    return {arc.source.name for arc in t.in_arcs}


def load_log_and_net(xes_path, pnml_path):
    log = xes_importer.apply(xes_path)
    net, im, fm = pm4py.read_pnml(pnml_path)
    return log, net, im, fm


def normalize_tau_labels(net):
    for t in net.transitions:
        if t.label and str(t.label).startswith("tau"):
            t.label = None


def replay_and_collect(log, net, im, fm):
    
    params = {
        "consider_remaining_in_fitness": False,
        "try_to_reach_final_marking_through_hidden": True,
        "walk_through_hidden_trans": True,
    }

    replay_results = token_replay.apply(log, net, im, fm, parameters=params)

    marking_transition_counts = defaultdict(int)  # (marking_key, transition_id) -> count
    marking_total_counts = defaultdict(int)       # marking_key -> total firings
    traces_used = 0
    traces_cut_early = 0

    for tr in replay_results:
        activated = tr.get("activated_transitions", [])
        if not activated:
            continue

        current_marking = im.copy()
        traces_used += 1

        for t in activated:
            # stop at first deviation
            if not is_enabled(current_marking, t):
                traces_cut_early += 1
                break

            m_key = marking_to_key(current_marking)
            t_id = transition_id(t)

            marking_transition_counts[(m_key, t_id)] += 1
            marking_total_counts[m_key] += 1

            current_marking = fire_transition(current_marking, t)

    return marking_transition_counts, marking_total_counts, traces_used, traces_cut_early


def compute_marking_transition_probabilities(marking_transition_counts, marking_total_counts):
    marking_transition_probabilities = defaultdict(dict)
    for (m_key, t_id), count in marking_transition_counts.items():
        total = marking_total_counts[m_key]
        marking_transition_probabilities[m_key][t_id] = count / total if total > 0 else 0.0
    return marking_transition_probabilities


def pretty_print_marking_probs(marking_transition_probabilities, traces_used, traces_cut_early):
    print("\n================ MARKING → TRANSITION PROBABILITIES (PREFIX-BASED, INCL. TAU) ================\n")
    print(f"Traces processed: {traces_used}")
    print(f"Traces cut early (non-enabled transition encountered): {traces_cut_early}\n")

    if not marking_transition_probabilities:
        print("No probabilities computed. (No activated transitions or everything deviated immediately.)")
        return

    for m_key in sorted(marking_transition_probabilities.keys(), key=lambda k: (len(k), k)):
        print("Marking:")
        if len(m_key) == 0:
            print("  (empty marking)")
        else:
            for place, tokens in m_key:
                print(f"  {place}: {tokens}")

        print("Transition probabilities:")
        for t_id, prob in sorted(marking_transition_probabilities[m_key].items(), key=lambda x: -x[1]):
            print(f"  {t_id}: {prob:.4f}")

        print("-" * 70)


def pretty_print_probs(prob_map):

    print(f"\n================ PLACE→TRANSITION ARC PROBABILITIES ================\n")
    if not prob_map:
        print("(empty)")
        return

    # Sort by place then descending prob
    def sort_key(item):
        k, v = item
        place = k.split("_", 1)[0] if "_" in k else k
        return (place, -v, k)

    for k, v in sorted(prob_map.items(), key=sort_key):
        print(f"{k}: {v:.4f}")


def build_place_transition_arc_prob_map(net,marking_transition_probabilities, marking_total_counts):
    t_by_id = {transition_id(t): t for t in net.transitions}

    num = defaultdict(float)   # (place_name, t_id) -> weighted sum
    denom = defaultdict(float) # place_name -> weighted sum

    for m_key, t_probs in marking_transition_probabilities.items():
        weight = marking_total_counts.get(m_key, 0)
        if weight <= 0:
            continue

        places_in_marking = {place_name for (place_name, tokens) in m_key if tokens > 0}

        preset_by_tid = {}
        for t_id in t_probs.keys():
            t_obj = t_by_id.get(t_id)
            if t_obj is None:
                continue
            preset_by_tid[t_id] = preset_place_names(t_obj)

        for p_name in places_in_marking:
            relevant_tids = [t_id for t_id, preset in preset_by_tid.items() if p_name in preset]
            if not relevant_tids:
                continue

            denom[p_name] += weight
            for t_id in relevant_tids:
                num[(p_name, t_id)] += t_probs[t_id] * weight

    arc_prob_map: Dict[str, float] = {}
    for (p_name, t_id), v in num.items():
        d = denom.get(p_name, 0.0)
        if d > 0:
            arc_prob_map[f"{p_name}_{t_id}"] = v / d

    return arc_prob_map

def fill_place_transition_arc_probs(json_path, arc_prob_map, decimals: int = 4):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "place_transition_arc" not in data or not isinstance(data["place_transition_arc"], dict):
        raise ValueError("JSON is missing a 'place_transition_arc' object or it is not a dict.")

    updated = 0
    for _, arcs in data["place_transition_arc"].items():
        if not isinstance(arcs, dict):
            continue

        for arc_key in list(arcs.keys()):
            if arc_key in arc_prob_map:
                arcs[arc_key] = f"{arc_prob_map[arc_key]:.{decimals}f}"
                updated += 1

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return data

def run_probability_mining_and_fill_config(pnml_path, xes_path, config_json_path):
    log, net, im, fm = load_log_and_net(xes_path, pnml_path)
    normalize_tau_labels(net)

    mt_counts, m_totals, traces_used, traces_cut_early = replay_and_collect(log, net, im, fm)
    m_probs = compute_marking_transition_probabilities(mt_counts, m_totals)


    arc_prob_map = build_place_transition_arc_prob_map(net, m_probs, m_totals)


    fill_place_transition_arc_probs(json_path=config_json_path, arc_prob_map=arc_prob_map, decimals=4)
