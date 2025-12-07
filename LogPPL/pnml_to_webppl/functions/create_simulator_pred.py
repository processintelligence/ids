def create_simulator_enabled_transitions_function(function_str, dpn, verbose, simulation_query):
    function_str += "var enabledTransitions = filter(function(x) {\nreturn "

    conditions = []
    for i, transition in enumerate(dpn.net.transitions):
        condition = f"(x == {i} && globalStore.enabled_{transition.name})"
        conditions.append(condition)

    joined_conditions = "||\n".join(conditions)
    indices = ", ".join(str(i) for i in range(len(dpn.net.transitions)))

    function_str += f"{joined_conditions};\n}}, [{indices}]);\n\n"

    function_str += """if (steps <= 0) {\nreturn;\n}\n\n"""
    function_str += """if (enabledTransitions.length == 0) {\nreturn;\n}\n\n"""

    if simulation_query == "final_marking":
        function_str += """if (globalStore.""" + str(list(dpn.final_marking.keys())[0]) + """ > 0) {\nreturn;\n}\n\n"""
    else:
        function_str += f"if ({simulation_query})" + "{\nreturn;\n}\n\n"

    return function_str


def create_simulator_sample_transition_function(function_str, net, verbose):
    function_str += """var transition = sample(Categorical({vs: enabledTransitions}));\n\n"""
    for i, transition in enumerate(net.transitions):
        if i == 0:
            function_str += f"if (transition == {i}) {{\n"
        else:
            function_str += f"else if (transition == {i}) {{\n"

        function_str += f"log_transition(\"{transition.label}\");\n"
        function_str += f"fire_{transition.name}();\n"
        function_str += "}\n"

    function_str += """else {\nconsole.log("Selected illegal transition; should never happen.");\n}\nsimulator_loop(steps - 1);\n}\n\n"""
    return function_str


def create_simulator_init_function(function_str, verbose):
    function_str += """var simulator_loop = function(steps) {\n\n"""
    function_str += """globalStore.xesOutput = "";\n\n"""
    return function_str


def create_simulator_loop_function(function_str, dpn, verbose, simulation_query):
    function_str = create_simulator_init_function(function_str, verbose)
    function_str = create_simulator_enabled_transitions_function(function_str, dpn, verbose, simulation_query)
    function_str = create_simulator_sample_transition_function(function_str, dpn.net, verbose)
    return function_str


def create_simulator_function(function_str, steps, sample_size, dpn, verbose, simulation_query):
    # INLINE ALL PREDICATES
    function_str = (
        "var Predicates = {};\n\n"
        "Predicates.firedNTimes = function(trace, id, n) {\n"
        "  return trace.counts[id] >= n;\n"
        "};\n\n"
        "Predicates.firedAtLeastOnce = function(trace, id) {\n"
        "  return trace.counts[id] >= 1;\n"
        "};\n\n"
        "Predicates.firedGroupAllOnce = function(trace, ids) {\n"
        "  for (var i = 0; i < ids.length; i++) {\n"
        "    if (trace.counts[ids[i]] < 1) {\n"
        "      return false;\n"
        "    }\n"
        "  }\n"
        "  return true;\n"
        "};\n\n"
    ) + function_str

    function_str += "var simulator = function(){\ninit();\n"

    for transition in dpn.net.transitions:
        function_str += f"update_enabled_{transition.name}();\n"

    function_str += "\n"
    function_str += """globalStore.trace += "<trace>\\n";\n\n"""
    function_str += f"simulator_loop({steps});\n\n"
    function_str += """globalStore.trace += "</trace>\\n";\n\n"""
    function_str += """console.log(globalStore.trace);\n\n"""

    # Return the trace object for predicates
    function_str += "return { counts: globalStore.counts, marking: globalStore.currentMarking };\n"
    function_str += "}\n\n"

    # MODEL WITH CONDITION
    predicate_expr = (
        "(Predicates.firedNTimes(trace, '4625_9_8_2_7_3', 5) && "
        "Predicates.firedAtLeastOnce(trace, '4657_common') && "
        "Predicates.firedGroupAllOnce(trace, ['4624_2', '4688_cmd', '4663']))"
    )

    function_str += (
        "var model = function() {\n"
        "  var trace = simulator();\n"
        f"  condition({predicate_expr});\n"
        "  return trace;\n"
        "};\n\n"
    )

    # INFERENCE ON MODEL
    function_str += (
        "var dist = Infer({\n"
        "  method: 'MCMC',\n"
        f"  samples: {sample_size},\n"
        "}, model);\n\n"
    )

    function_str += "// Extract the samples\n"
    function_str += "var samplesArray = dist.samples;\n"
    function_str += "var params = dist.params;\n\n"
    function_str += """var jsonString = JSON.stringify({ "dist": dist });\n\n"""
    function_str += "jsonString;\n"

    return function_str
