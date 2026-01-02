import importlib

import LogPPL.pnml_to_webppl.functions.create_init as init_function
import LogPPL.pnml_to_webppl.functions.create_enabler as enabler_function
from LogPPL.pnml_to_webppl.dpn import DPN
from LogPPL.pnml_to_webppl.functions.create_logging import create_logging as logging_function
#from LogPPL.pnml_to_webppl.functions.create_simulator_pred import create_simulator_function, create_simulator_loop_function
#from LogPPL.pnml_to_webppl.functions.create_simulator import create_simulator_function, create_simulator_loop_function
import LogPPL.pnml_to_webppl.functions.create_firing as firing_function
from LogPPL.pnml_to_webppl.functions import utils_string


def convert_dpn_to_webPPL(path, verbose, simulation_steps, sample_size, simulation_query, distributions={}, attacktype=None,):
    dpn = DPN(path,distributions)

    dpn = utils_string.string_to_long(dpn)

    #conditional import
    simulator_module_name = (
        "LogPPL.pnml_to_webppl.functions.create_simulator_pred"
        if attacktype is not None
        else "LogPPL.pnml_to_webppl.functions.create_simulator"
    )
    simulator = importlib.import_module(simulator_module_name)

    # Create Initial Function
    function_str = init_function.create_init_function(dpn, verbose)

    # Create Enabler Function
    function_str = enabler_function.create_enabler_function(function_str, dpn, verbose)

    # Create Firings Function
    print("FIRING")
    function_str += firing_function.generate_firings(dpn)

    # Create Logging
    function_str = logging_function(function_str, dpn, verbose)

    # Create Simulator Loop Function
    function_str = simulator.create_simulator_loop_function(function_str, dpn, verbose, simulation_query)

    # Create Simulation Function
    function_str = simulator.create_simulator_function(function_str, simulation_steps, sample_size, dpn, verbose, simulation_query, attacktype) 
    return function_str
