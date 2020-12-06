import logging
from pathlib import Path
from fortress.detectors.variables.unused_state_variables import UnusedStateVars
from fortress.detectors.attributes.incorrect_solc import IncorrectSolc
from fortress.detectors.attributes.constant_pragma import ConstantPragma
from fortress.detectors.naming_convention.naming_convention import NamingConvention
from fortress.detectors.functions.external_function import ExternalFunction
from fortress.detectors.variables.possible_const_state_variables import ConstCandidateStateVars
from fortress.detectors.attributes.const_functions_asm import ConstantFunctionsAsm
from fortress.detectors.attributes.const_functions_state import ConstantFunctionsState
from fortress.utils.colors import yellow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Fortress.Format")

all_detectors = {
    "unused-state": UnusedStateVars,
    "solc-version": IncorrectSolc,
    "pragma": ConstantPragma,
    "naming-convention": NamingConvention,
    "external-function": ExternalFunction,
    "constable-states": ConstCandidateStateVars,
    "constant-function-asm": ConstantFunctionsAsm,
    "constant-functions-state": ConstantFunctionsState,
}


def fortress_format(fortress, **kwargs):  # pylint: disable=too-many-locals
    """'
    Keyword Args:
        detectors_to_run (str): Comma-separated list of detectors, defaults to all
    """

    detectors_to_run = choose_detectors(
        kwargs.get("detectors_to_run", "all"), kwargs.get("detectors_to_exclude", "")
    )

    for detector in detectors_to_run:
        fortress.register_detector(detector)

    fortress.generate_patches = True

    detector_results = fortress.run_detectors()
    detector_results = [x for x in detector_results if x]  # remove empty results
    detector_results = [item for sublist in detector_results for item in sublist]  # flatten

    export = Path("crytic-export", "patches")

    export.mkdir(parents=True, exist_ok=True)

    counter_result = 0

    logger.info(yellow("fortress-format is in beta, carefully review each patch before merging it."))

    for result in detector_results:
        if not "patches" in result:
            continue
        one_line_description = result["description"].split("\n")[0]

        export_result = Path(export, f"{counter_result}")
        export_result.mkdir(parents=True, exist_ok=True)
        counter_result += 1
        counter = 0

        logger.info(f"Issue: {one_line_description}")
        logger.info(f"Generated: ({export_result})")

        for (_, diff,) in result["patches_diff"].items():
            filename = f"fix_{counter}.patch"
            path = Path(export_result, filename)
            logger.info(f"\t- {filename}")
            with open(path, "w") as f:
                f.write(diff)
            counter += 1


# endregion
###################################################################################
###################################################################################
# region Detectors
###################################################################################
###################################################################################


def choose_detectors(detectors_to_run, detectors_to_exclude):
    # If detectors are specified, run only these ones
    cls_detectors_to_run = []
    exclude = detectors_to_exclude.split(",")
    if detectors_to_run == "all":
        for d in all_detectors:
            if d in exclude:
                continue
            cls_detectors_to_run.append(all_detectors[d])
    else:
        exclude = detectors_to_exclude.split(",")
        for d in detectors_to_run.split(","):
            if d in all_detectors:
                if d in exclude:
                    continue
                cls_detectors_to_run.append(all_detectors[d])
            else:
                raise Exception("Error: {} is not a detector".format(d))
    return cls_detectors_to_run


# endregion
###################################################################################
###################################################################################
# region Debug functions
###################################################################################
###################################################################################


def print_patches(number_of_fortress_results, patches):
    logger.info("Number of Fortress results: " + str(number_of_fortress_results))
    number_of_patches = 0
    for file in patches:
        number_of_patches += len(patches[file])
    logger.info("Number of patches: " + str(number_of_patches))
    for file in patches:
        logger.info("Patch file: " + file)
        for patch in patches[file]:
            logger.info("Detector: " + patch["detector"])
            logger.info("Old string: " + patch["old_string"].replace("\n", ""))
            logger.info("New string: " + patch["new_string"].replace("\n", ""))
            logger.info("Location start: " + str(patch["start"]))
            logger.info("Location end: " + str(patch["end"]))


def print_patches_json(number_of_fortress_results, patches):
    print("{", end="")
    print('"Number of Fortress results":' + '"' + str(number_of_fortress_results) + '",')
    print('"Number of patchlets":' + '"' + str(len(patches)) + '"', ",")
    print('"Patchlets":' + "[")
    for index, file in enumerate(patches):
        if index > 0:
            print(",")
        print("{", end="")
        print('"Patch file":' + '"' + file + '",')
        print('"Number of patches":' + '"' + str(len(patches[file])) + '"', ",")
        print('"Patches":' + "[")
        for inner_index, patch in enumerate(patches[file]):
            if inner_index > 0:
                print(",")
            print("{", end="")
            print('"Detector":' + '"' + patch["detector"] + '",')
            print('"Old string":' + '"' + patch["old_string"].replace("\n", "") + '",')
            print('"New string":' + '"' + patch["new_string"].replace("\n", "") + '",')
            print('"Location start":' + '"' + str(patch["start"]) + '",')
            print('"Location end":' + '"' + str(patch["end"]) + '"')
            if "overlaps" in patch:
                print('"Overlaps":' + "Yes")
            print("}", end="")
        print("]", end="")
        print("}", end="")
    print("]", end="")
    print("}")