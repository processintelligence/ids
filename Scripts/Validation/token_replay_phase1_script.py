import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.objects.log.obj import Event
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator


pmnl_path = r"INPUT PHASE 1 NET" #TODO: PHASE 1 net

real_xes = r"LosAlamos/wls_800MB.xes"

log = xes_importer.apply(real_xes)

for trace in log:
    trace._list = [evt for evt in trace if evt.get("concept:name") != "init_t"]

for trace in log:
    new_event = Event({"concept:name": "4608"}) #TODO: If we change in lucid this does not matter
    trace.insert(0, new_event)


net, im, fm = pm4py.read_pnml(pmnl_path)

# Ignore silent transition
for t in net.transitions:
    if t.label and str(t.label).startswith("tau"):
        t.label = None 

params = {
    # Do not consider remaining tokens in the fitness calculation:
    "consider_remaining_in_fitness": False,
    "try_to_reach_final_marking_through_hidden": True,
    "walk_through_hidden_trans": True
}


results = token_replay.apply(log, net, im, fm, parameters=params)

trace_fitnesses = [r["trace_fitness"] for r in results]
print("Average fitness:", sum(trace_fitnesses) / len(trace_fitnesses))
print("Min fitness:", min(trace_fitnesses))
print("Max fitness:", max(trace_fitnesses))

bad_traces = [log[i] for i, r in enumerate(results) if not r["trace_is_fit"]]
print("Number of bad traces:", len(bad_traces))

exclude_trace = ["4608", "4672", "4624_3", "4634_3"]
exclude_trace2 = ["4608", "4672", "4624_3"]

filtered_bad_traces = []
for trace in bad_traces:
    trace_seq = [evt["concept:name"] for evt in trace]
    if trace_seq != exclude_trace and trace_seq != exclude_trace2:
        filtered_bad_traces.append(trace)

print("Number of bad traces after excluding the target trace:", len(filtered_bad_traces))

# Print all filtered bad traces
for i, trace in enumerate(filtered_bad_traces):
    print(f"\n=== Bad Trace #{i+1} ===")
    for event in trace:
        print(event["concept:name"])
