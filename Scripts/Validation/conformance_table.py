from .evaluation_metrics import compute_alignment_fitness
import os

"""
pmnl_paths = [
    "Scripts/Phase_2/PetriNet/pnml/phase_2_benign_extended.pnml",
    "Scripts/Phase_3/PetriNet/pnml/phase_3_redflag.pnml",
    "Scripts/Phase_3/PetriNet/pnml/phase_3_repeat.pnml",
]

xes_paths = [
    "GeneratedFiles/csv_xes/Benign.xes",
    "GeneratedFiles/csv_xes/RedFlag.xes",
    "GeneratedFiles/csv_xes/Repeat.xes",
]
"""
"""
pmnl_paths = [
    "Scripts/Phase_2/PetriNet/pnml/phase_2_benign_extended.pnml",
    "Scripts/Phase_2/PetriNet/pnml/phase_2_redflag.pnml",
    "Scripts/Phase_2/PetriNet/pnml/phase_2_repeat.pnml",
    "Scripts/Phase_2/PetriNet/pnml/phase_2_composite.pnml",
]

xes_paths = [
    "GeneratedFiles/csv_xes/Benign.xes",
    "GeneratedFiles/csv_xes/RedFlag.xes",
    "GeneratedFiles/csv_xes/Repeat.xes",
    "GeneratedFiles/csv_xes/Composite.xes",
]
"""
pmnl_paths = [
    "Scripts/Phase_1/pnml/phase_1_benign.pnml",
    "Scripts/Phase_1/pnml/phase_1_redflag.pnml",
    "Scripts/Phase_1/pnml/phase_1_repeat.pnml",
    "Scripts/Phase_1/pnml/phase_1_composite.pnml",
]

xes_paths = [
    "GeneratedFiles/WebPPL_XES/data_phase_1_benign.xes",
    "GeneratedFiles/WebPPL_XES/data_phase_1_redflag.xes",
    "GeneratedFiles/WebPPL_XES/data_phase_1_repeat.xes",
    "GeneratedFiles/WebPPL_XES/data_phase_1_composite.xes",
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


if __name__ == "__main__":
    # Dict: {pmnl_name: {xes_name: fitness}}
    conformance_table = {}

    for pmnl_path in pmnl_paths:
        pmnl_name = os.path.basename(pmnl_path).replace('.pnml', '  ').replace('phase_3_', '').replace('phase_2_', '').replace('_extended', '')

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
