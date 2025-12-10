import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.objects.log.obj import Event


xes_path = r"C:\Users\lomo0\Documents\GitHub\MasterRepo\MasterRepo\GeneratedFiles\WebPPL_XES\data_phase_1_net.xes"
pmnl_path = r"C:\Users\lomo0\Documents\GitHub\MasterRepo\MasterRepo\PNMLFiles\phase_1_net.pnml"

real_xes  = r"C:\Users\lomo0\Documents\RandomScripts\wls_processtype_PROM.xes"

real_xes_2 = r"c:\Users\lomo0\Documents\RandomScripts\wls_800MB.xes"

log = xes_importer.apply(real_xes)

for trace in log:
    trace._list = [evt for evt in trace if evt.get("concept:name") != "init_t"]

for trace in log:
    new_event = Event({"concept:name": "4608"})
    trace.insert(0, new_event)


net, im, fm = pm4py.read_pnml(pmnl_path)

for t in net.transitions:
    if t.label and str(t.label).startswith("tau"):
        t.label = None   # invisible transitions

params = {
    # do not consider remaining tokens in the fitness calculation:
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
""" for i, trace in enumerate(filtered_bad_traces):
    print(f"\n=== Bad Trace #{i+1} ===")
    for event in trace:
        print(event["concept:name"]) """
