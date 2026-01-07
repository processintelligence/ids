import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from collections import defaultdict
from pm4py.objects.log.obj import Event


# PATHS
XES_PATH = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/csv_xes/smaller_script_clean_test.xes"
PNML_PATH = "/Users/emilpontoppidanrasmussen/Desktop/master/MasterRepo/GeneratedFiles/PNML/heuristics_test1.pnml"

# LOAD LOG
log = xes_importer.apply(XES_PATH)

#leave out init_t
for trace in log:
    trace._list = [evt for evt in trace if evt.get("concept:name") != "init_t"]

#this code is only important 
#for trace in log:
#    new_event = Event({"concept:name": "4608"})
#    trace.insert(0, new_event)


# instantiate petrinet 
net, im, fm = pm4py.read_pnml(PNML_PATH)

# make tau invisible - should be alright but double checking
for t in net.transitions:
    if t.label and str(t.label).startswith("tau"):
        t.label = None


# TOKEN REPLAY
params = {
    "consider_remaining_in_fitness": False, #we dont want penalize unfinished traces
    "try_to_reach_final_marking_through_hidden": True,
    "walk_through_hidden_trans": True
}

replay_results = token_replay.apply(log, net, im, fm, parameters=params)


def marking_to_key(marking):
    #returns a marking on hte form (place, token_count)
    return tuple(sorted((p.name, marking[p]) for p in marking if marking[p] > 0))


def fire_transition(marking, transition):
    # fires the transition and returns the new
    new_marking = marking.copy()

    # consume tokens
    for arc in transition.in_arcs:
        src = arc.source
        new_marking[src] -= 1
        if new_marking[src] == 0:
            del new_marking[src]

    # produce tokens
    for arc in transition.out_arcs:
        tgt = arc.target
        new_marking[tgt] = new_marking.get(tgt, 0) + 1

    return new_marking


def transition_id(t):
    #returns label for a transition
    return t.label if t.label is not None else f"tau::{t.name}"


#in a given marking, how many times is a specific transition fired
marking_transition_counts = defaultdict(int)
#in a given marking, how many times is any transition fired
marking_total_counts = defaultdict(int)

for trace_result in replay_results:
    if not trace_result.get("trace_is_fit", False):
        continue  # only use fitting traces

    current_marking = im.copy()

    for t in trace_result["activated_transitions"]:
        m_key = marking_to_key(current_marking)
        t_id = transition_id(t)

        marking_transition_counts[(m_key, t_id)] += 1
        marking_total_counts[m_key] += 1

        current_marking = fire_transition(current_marking, t)


# COMPUTE PROBABILITIES
marking_transition_probabilities = defaultdict(dict)

for (m_key, t_id), count in marking_transition_counts.items():
    total = marking_total_counts[m_key]
    marking_transition_probabilities[m_key][t_id] = count / total if total > 0 else 0.0


#MAIN  OR CLI
# OUTPUT RESULTS
print("\n================ MARKING → TRANSITION PROBABILITIES (INCLUDING TAU) ================\n")

# sort markings for nicer output
for m_key in sorted(marking_transition_probabilities.keys(), key=lambda k: (len(k), k)):

    print("Marking:")
    if len(m_key) == 0:
        print("  (empty marking)")
    else:
        for place, tokens in m_key:
            print(f"  {place}: {tokens}")

    print("Transition probabilities:")
    transitions = marking_transition_probabilities[m_key]
    for t_id, prob in sorted(transitions.items(), key=lambda x: -x[1]):
        print(f"  {t_id}: {prob:.4f}")

    print("-" * 70)
