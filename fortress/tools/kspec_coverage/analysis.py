import re
import logging

from fortress.core.declarations import Function
from fortress.core.variables.variable import Variable
from fortress.utils.colors import yellow, green, red
from fortress.utils import output

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("Fortress.kspec")


# pylint: disable=anomalous-backslash-in-string


def _refactor_type(targeted_type):
    return {"uint": "uint256", "int": "int256"}.get(targeted_type, targeted_type)


def _get_all_covered_kspec_functions(target):
    # Create a set of our discovered functions which are covered
    covered_functions = set()

    BEHAVIOUR_PATTERN = re.compile("behaviour\s+(\S+)\s+of\s+(\S+)")
    INTERFACE_PATTERN = re.compile("interface\s+([^\r\n]+)")

    # Read the file contents
    with open(target, "r", encoding="utf8") as target_file:
        lines = target_file.readlines()

    # Loop for each line, if a line matches our behaviour regex, and the next one matches our interface regex,
    # we add our finding
    i = 0
    while i < len(lines):
        match = BEHAVIOUR_PATTERN.match(lines[i])
        if match:
            contract_name = match.groups()[1]
            match = INTERFACE_PATTERN.match(lines[i + 1])
            if match:
                function_full_name = match.groups()[0]
                start, end = (
                    function_full_name.index("(") + 1,
                    function_full_name.index(")"),
                )
                function_arguments = function_full_name[start:end].split(",")
                function_arguments = [
                    _refactor_type(arg.strip().split(" ")[0]) for arg in function_arguments
                ]
                function_full_name = function_full_name[:start] + ",".join(function_arguments) + ")"
                covered_functions.add((contract_name, function_full_name))
                i += 1
        i += 1
    return covered_functions


def _get_fortress_functions(fortress):
    # Use contract == contract_declarer to avoid dupplicate
    all_functions_declared = [
        f
        for f in fortress.functions
        if (
            f.contract == f.contract_declarer
            and f.is_implemented
            and not f.is_constructor
            and not f.is_constructor_variables
        )
    ]
    # Use list(set()) because same state variable instances can be shared accross contracts
    # TODO: integrate state variables
    all_functions_declared += list(
        {s for s in fortress.state_variables if s.visibility in ["public", "external"]}
    )
    fortress_functions = {
        (function.contract.name, function.full_name): function
        for function in all_functions_declared
    }

    return fortress_functions


def _generate_output(kspec, message, color, generate_json):
    info = ""
    for function in kspec:
        info += f"{message} {function.contract.name}.{function.full_name}\n"
    if info:
        logger.info(color(info))

    if generate_json:
        json_kspec_present = output.Output(info)
        for function in kspec:
            json_kspec_present.add(function)
        return json_kspec_present.data
    return None


def _generate_output_unresolved(kspec, message, color, generate_json):
    info = ""
    for contract, function in kspec:
        info += f"{message} {contract}.{function}\n"
    if info:
        logger.info(color(info))

    if generate_json:
        json_kspec_present = output.Output(info, additional_fields={"signatures": kspec})
        return json_kspec_present.data
    return None


def _run_coverage_analysis(args, fortress, kspec_functions):
    # Collect all fortress functions
    fortress_functions = _get_fortress_functions(fortress)

    # Determine which klab specs were not resolved.
    fortress_functions_set = set(fortress_functions)
    kspec_functions_resolved = kspec_functions & fortress_functions_set
    kspec_functions_unresolved = kspec_functions - kspec_functions_resolved

    kspec_missing = []
    kspec_present = []

    for fortress_func_desc in sorted(fortress_functions_set):
        fortress_func = fortress_functions[fortress_func_desc]

        if fortress_func_desc in kspec_functions:
            kspec_present.append(fortress_func)
        else:
            kspec_missing.append(fortress_func)

    logger.info("## Check for functions coverage")
    json_kspec_present = _generate_output(kspec_present, "[✓]", green, args.json)
    json_kspec_missing_functions = _generate_output(
        [f for f in kspec_missing if isinstance(f, Function)],
        "[ ] (Missing function)",
        red,
        args.json,
    )
    json_kspec_missing_variables = _generate_output(
        [f for f in kspec_missing if isinstance(f, Variable)],
        "[ ] (Missing variable)",
        yellow,
        args.json,
    )
    json_kspec_unresolved = _generate_output_unresolved(
        kspec_functions_unresolved, "[ ] (Unresolved)", yellow, args.json
    )

    # Handle unresolved kspecs
    if args.json:
        output.output_to_json(
            args.json,
            None,
            {
                "functions_present": json_kspec_present,
                "functions_missing": json_kspec_missing_functions,
                "variables_missing": json_kspec_missing_variables,
                "functions_unresolved": json_kspec_unresolved,
            },
        )


def run_analysis(args, fortress, kspec_arg):
    # Get all of our kspec'd functions (tuple(contract_name, function_name)).
    if "," in kspec_arg:
        kspecs = kspec_arg.split(",")
        kspec_functions = set()
        for kspec in kspecs:
            kspec_functions |= _get_all_covered_kspec_functions(kspec)
    else:
        kspec_functions = _get_all_covered_kspec_functions(kspec_arg)

    # Run coverage analysis
    _run_coverage_analysis(args, fortress, kspec_functions)
