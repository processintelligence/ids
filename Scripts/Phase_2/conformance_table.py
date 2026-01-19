from ..Validation.evaluation_metrics import compute_alignment_fitness
import os

pmnl_paths = [
    r"Scripts\Phase_2\PetriNet\pnml\phase_2_benign.pnml",
    r"Scripts\Phase_2\PetriNet\pnml\phase_2_redflag.pnml",
    r"Scripts\Phase_2\PetriNet\pnml\phase_2_repeat.pnml",
    r"Scripts\Phase_2\PetriNet\pnml\phase_2_composite.pnml"
]

xes_paths = [
    r"C:\Users\lomo0\Downloads\AttackLogsPhase2\Benign.xes",
    r"C:\Users\lomo0\Downloads\AttackLogsPhase2\RedFlag.xes",
    r"C:\Users\lomo0\Downloads\AttackLogsPhase2\Repeat.xes",
    r"C:\Users\lomo0\Downloads\AttackLogsPhase2\Composite.xes"
]


def print_conformance_table(conformance_table, xes_paths):
    print("Conformance Table (Fitness)")
    print("=" * 50)

    header = "PMNL/XES\t" + "\t".join([os.path.basename(x).replace('.xes', '') for x in xes_paths])
    print(header)

    for pmnl_name in conformance_table:
        row = pmnl_name + "\t"
        for xes_name in conformance_table[pmnl_name]:
            value = conformance_table[pmnl_name][xes_name]
            row += f"{value:.3f}\t" if value is not None else "N/A\t"
        print(row)


# Dict: {pmnl_name: {xes_name: fitness}}
conformance_table = {}

for pmnl_path in pmnl_paths:
    pmnl_name = os.path.basename(pmnl_path).replace('.pnml', '  ').replace('phase_2_', '')
    conformance_table[pmnl_name] = {}
    for xes_path in xes_paths:
        xes_name = os.path.basename(xes_path).replace('.xes', '')
        try:
            fitness = compute_alignment_fitness(pmnl_path, xes_path)
            conformance_table[pmnl_name][xes_name] = fitness
        except Exception as e:
            print(f"Error computing fitness for {pmnl_name} and {xes_name}: {e}")
            conformance_table[pmnl_name][xes_name] = None

print_conformance_table(conformance_table, xes_paths)
