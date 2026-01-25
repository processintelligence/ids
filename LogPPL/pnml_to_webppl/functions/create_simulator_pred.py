# =============================================================================
# Attribution
# -----------------------------------------------------------------------------
# 2026 Emil Pontoppidan Rasmussen (s204441) and Emil Løvstrand Mortensen (s204483).
# This code extends prior work by Rivkin et al.
#
# Portions of the simulator-generation pipeline are adapted/derived from the
# Rivkin et al. codebase.
# =============================================================================
#TODO: FIX ET AL


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

        function_str += f'log_transition("{transition.label}");\n'
        function_str += f'recordEvent("{transition.label}");\n'
        function_str += f'incrementCount("{transition.label}");\n'
        function_str += f"fire_{transition.name}();\n"
        function_str += "}\n"

    function_str += (
        'else {\nconsole.log("Selected illegal transition; should never happen.");\n}\n'
        "simulator_loop(steps - 1);\n"
        "}\n\n"
    )
    return function_str


def create_simulator_init_function(function_str, verbose):
    function_str += "var simulator_loop = function(steps) {\n\n"
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
        # COUNT-BASED HELPERS
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
        "var hasToFinish = function() {\n"
        "  var ids = ['4634_3', '4634_5', '4634_2_7_8_9', '4634_2'];\n"
        "  var helper = function(index) {\n"
        "    if (index >= ids.length) {\n"
        "      return false;\n"
        "    }\n"
        "    var key = 'count_' + ids[index];\n"
        "    var c = globalStore[key] || 0;\n"
        "    if (c >= 1) {\n"
        "      return true;\n"
        "    }\n"
        "    return helper(index + 1);\n"
        "  };\n"
        "  return helper(0);\n"
        "};\n\n"
        "var hasToLogIn = function() {\n"
        "  var ids = ['4624_2', '4624_3', '4624_9', '4624_8', '4624_7'];\n"
        "  var helper = function(index) {\n"
        "    if (index >= ids.length) {\n"
        "      return false;\n"
        "    }\n"
        "    var key = 'count_' + ids[index];\n"
        "    var c = globalStore[key] || 0;\n"
        "    if (c >= 1) {\n"
        "      return true;\n"
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
        "\n"


        # SEQUENCE-BASED HELPERS
        "var recordEvent = function(label) {\n"
        "  if (globalStore.eventSeq === undefined) {\n"
        "    globalStore.eventSeq = [];\n"
        "  }\n"
        "  globalStore.eventSeq = globalStore.eventSeq.concat([label]);\n"
        "};\n\n"
        "\n"
        "var maxRunLength = function(label) {\n"
        "  var xs = globalStore.eventSeq || [];\n"
        "  var go = function(i, cur, best) {\n"
        "    if (i >= xs.length) { return best; }\n"
        "    var cur2 = (xs[i] === label) ? (cur + 1) : 0;\n"
        "    var best2 = (cur2 > best) ? cur2 : best;\n"
        "    return go(i + 1, cur2, best2);\n"
        "  };\n"
        "  return go(0, 0, 0);\n"
        "};\n\n"
        "\n"
        "var firedAtLeastYInARow = function(trace, label, y) {\n"
        "  return maxRunLength(label) >= y;\n"
        "};\n\n"
        "\n"
        "var happensBefore = function(trace, a, b) {\n"
        "  var xs = globalStore.eventSeq || [];\n"
        "  var findFirst = function(label, i) {\n"
        "    if (i >= xs.length) { return -1; }\n"
        "    if (xs[i] === label) { return i; }\n"
        "    return findFirst(label, i + 1);\n"
        "  };\n"
        "  var ia = findFirst(a, 0);\n"
        "  var ib = findFirst(b, 0);\n"
        "  return (ia !== -1) && (ib !== -1) && (ia < ib);\n"
        "};\n\n"
        "\n"
        "var existsNotFollowedBy = function(trace, c, d) {\n"
        "  var xs = globalStore.eventSeq || [];\n"
        "  var go = function(i) {\n"
        "    if (i >= xs.length) { return false; }\n"
        "    if (xs[i] === c) {\n"
        "      if (i === xs.length - 1) { return true; }\n"
        "      if (xs[i + 1] !== d) { return true; }\n"
        "    }\n"
        "    return go(i + 1);\n"
        "  };\n"
        "  return go(0);\n"
        "};\n\n"
    ) + function_str


    function_str += "var simulator = function(){\ninit();\n"

    function_str += "globalStore.eventSeq = [];\n"

    function_str += "globalStore.trace = '';\n"
    function_str += "globalStore.xesOutput = '';\n\n"

    for transition in dpn.net.transitions:
        function_str += f'globalStore["count_{transition.label}"] = 0;\n'

    for transition in dpn.net.transitions:
        function_str += f"update_enabled_{transition.name}();\n"

    function_str += "\n"
    function_str += "globalStore.trace += '<trace>\\n';\n"
    function_str += "globalStore.xesOutput += '<trace>\\n';\n\n"
    function_str += f"simulator_loop({steps});\n\n"
    function_str += "globalStore.trace += '</trace>\\n';\n"
    function_str += "globalStore.xesOutput += '</trace>\\n';\n\n"

    function_str += (
        "if (globalStore.xesOutput && globalStore.xesOutput.length > 0) {\n"
        "  console.log(globalStore.xesOutput);\n"
        "} else {\n"
        "  console.log(globalStore.trace);\n"
        "}\n\n"
    )

    function_str += "return { marking: globalStore.currentMarking };\n"
    function_str += "};\n\n"

    # Predicate maps 
    predicate_expr_map = {
        # sequence-aware predicates 
        "Repeat": "hasToFinish() && hasToLogIn() && firedAtLeastYInARow(trace, '4625', 5)",
        "Redflag": "hasToFinish() && firedAtLeastOnce(trace, '4657_common')",
        "Composite": (
            "hasToFinish() && "
            "firedAtLeastOnce(trace, '4624_4') && "
            "firedAtLeastOnce(trace, '4688_cmd') && "
            "firedAtLeastOnce(trace, '4657') && "
            "happensBefore(trace, '4624_4', '4688_cmd') && "
            "happensBefore(trace, '4624_4', '4657') && "
            "existsNotFollowedBy(trace, '4663', '4657')"
        ),
        "4th": (
            "hasToFinish() && "
            "firedAtLeastOnce(trace, '4688_passworddll') && "
            "firedAtLeastOnce(trace, '4657_lsa')"
        )
    }


    predicate_expr = predicate_expr_map.get(attacktype, "true")

    function_str += (
        "var model = function() {\n"
        "  var trace = simulator();\n"
        f"  condition({predicate_expr});\n"
        "  return trace;\n"
        "};\n\n"
    )

    # inference
    function_str += (
        "var dist = Infer({\n"
        "  method: 'MCMC',\n"
        f"  samples: {sample_size},\n"
        "}, model);\n\n"
    )

    function_str += "// Extract the samples\n"
    function_str += "var samplesArray = dist.samples;\n"
    function_str += "var params = dist.params;\n\n"
    function_str += 'var jsonString = JSON.stringify({ "dist": dist });\n\n'
    function_str += "jsonString;\n"

    return function_str
