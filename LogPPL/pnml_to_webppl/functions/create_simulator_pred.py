def create_simulator_enabled_transitions_function(function_str, dpn, verbose, simulation_query):
    function_str += "var enabledTransitions = filter(function(x) {\nreturn "

    conditions = []
    for i, transition in enumerate(dpn.net.transitions):
        condition = f"(x == {i} && globalStore.enabled_{transition.name})"
        conditions.append(condition)

    joined_conditions = "||\n".join(conditions)
    indices = ", ".join(str(i) for i in range(len(dpn.net.transitions)))

    function_str += f"{joined_conditions};\n}}, [{indices}]);\n\n"

    function_str += "if (steps <= 0) {\nreturn;\n}\n\n"
    function_str += "if (enabledTransitions.length == 0) {\nreturn;\n}\n\n"

    if simulation_query == "final_marking":
        function_str += (
            "if (globalStore."
            + str(list(dpn.final_marking.keys())[0])
            + " > 0) {\nreturn;\n}\n\n"
        )
    else:
        function_str += f"if ({simulation_query})" + "{\nreturn;\n}\n\n"

    return function_str


def create_simulator_sample_transition_function(function_str, net, verbose):
    function_str += "var transition = sample(Categorical({vs: enabledTransitions}));\n\n"
    for i, transition in enumerate(net.transitions):
        if i == 0:
            function_str += f"if (transition == {i}) {{\n"
        else:
            function_str += f"else if (transition == {i}) {{\n"

        # Log transition to XES
        function_str += f'log_transition("{transition.label}");\n'
        # Increment count for this label in globalStore
        function_str += f'incrementCount("{transition.label}");\n'
        # Fire the transition
        function_str += f"fire_{transition.name}();\n"
        function_str += "}\n"

    function_str += (
        'else {\nconsole.log("Selected illegal transition; should never happen.");\n}'
        "\nsimulator_loop(steps - 1);\n}\n\n"
    )
    return function_str


def create_simulator_init_function(function_str, verbose):
    function_str += "var simulator_loop = function(steps) {\n\n"
    function_str += 'globalStore.xesOutput = "";\n\n'
    return function_str


def create_simulator_loop_function(function_str, dpn, verbose, simulation_query):
    function_str = create_simulator_init_function(function_str, verbose)
    function_str = create_simulator_enabled_transitions_function(
        function_str, dpn, verbose, simulation_query
    )
    function_str = create_simulator_sample_transition_function(
        function_str, dpn.net, verbose
    )
    return function_str


def create_simulator_function(function_str, steps, sample_size, dpn, verbose, simulation_query, attacktype):
    function_str = (
        "var firedNTimes = function(trace, id, n) {\n"
        "  var key = 'count_' + id;\n"
        "  var c = globalStore[key] || 0;\n"
        "  return c >= n;\n"
        "};\n\n"
        "var firedAtLeastOnce = function(trace, id) {\n"
        "  var key = 'count_' + id;\n"
        "  var c = globalStore[key] || 0;\n"
        "  return c >= 1;\n"
        "};\n\n"
        "var firedGroupAllOnce = function(trace, ids) {\n"
        "  var helper = function(index) {\n"
        "    if (index >= ids.length) {\n"
        "      return true;\n"
        "    }\n"
        "    var key = 'count_' + ids[index];\n"
        "    var c = globalStore[key] || 0;\n"
        "    if (c < 1) {\n"
        "      return false;\n"
        "    }\n"
        "    return helper(index + 1);\n"
        "  };\n"
        "  return helper(0);\n"
        "};\n\n"
        "var incrementCount = function(label) {\n"
        "  var key = 'count_' + label;\n"
        "  if (globalStore[key] === undefined) {\n"
        "    globalStore[key] = 0;\n"
        "  }\n"
        "  globalStore[key] += 1;\n"
        "};\n\n"
    ) + function_str

    # Simulator wrapper
    function_str += "var simulator = function(){\ninit();\n"

    # Reset all counts for this run (per transition label)
    for transition in dpn.net.transitions:
        function_str += f'globalStore["count_{transition.label}"] = 0;\n'

    # Initialize enabled transitions once
    for transition in dpn.net.transitions:
        function_str += f"update_enabled_{transition.name}();\n"

    function_str += "\n"
    function_str += 'globalStore.trace += "<trace>\\n";\n\n'
    function_str += f"simulator_loop({steps});\n\n"
    function_str += 'globalStore.trace += "</trace>\\n";\n\n'
    function_str += "console.log(globalStore.trace);\n\n"

    # Return a simple trace object (marking only; predicates use globalStore counts)
    function_str += "return { marking: globalStore.currentMarking };\n"
    function_str += "}\n\n"

    # MODEL WITH CONDITION
    predicate_expr_map = {
        "Repeat": "firedNTimes(trace, '4625_9_8_2_7_3', 5)",
        "Redflag": "firedAtLeastOnce(trace, '4657_common')",
        "Composite": "firedGroupAllOnce(trace, ['4624_4', '4688_cmd', '4663', '4657_registry'])",
    }

    predicate_expr = predicate_expr_map.get(attacktype, "true")


    function_str += (
        "var model = function() {\n"
        "  var trace = simulator();\n"
        f"  condition({predicate_expr});\n"
        "  return trace;\n"
        "};\n\n"
    )

    #INFERENCE ON MCMC
    function_str += (
        "var dist = Infer({\n"
        "  method: 'MCMC',\n"
        f"  samples: {sample_size},\n"
        "}, model);\n\n"
)

    # INFERENCE ON SMC
    #function_str += (
    #    "var dist = Infer({\n"
    #    "  method: 'SMC',\n"
    #    f"  particles: {sample_size},\n"
    #    "}, model);\n\n"
    #)


    function_str += "// Extract the samples\n"
    function_str += "var samplesArray = dist.samples;\n"
    function_str += "var params = dist.params;\n\n"
    function_str += 'var jsonString = JSON.stringify({ "dist": dist });\n\n'
    function_str += "jsonString;\n"

    return function_str
