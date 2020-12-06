import sys
import argparse
import logging
from crytic_compile import cryticparser
from fortress import Fortress
from fortress.utils.command_line import read_config_file
from fortress.tools.fortress_format.fortress_format import fortress_format


logging.basicConfig()
logging.getLogger("Fortress").setLevel(logging.INFO)

# Fortress detectors for which fortress-format currently works
available_detectors = [
    "unused-state",
    "solc-version",
    "pragma",
    "naming-convention",
    "external-function",
    "constable-states",
    "constant-function-asm",
    "constatnt-function-state",
]


def parse_args():
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    parser = argparse.ArgumentParser(description="fortress_format", usage="fortress_format filename")

    parser.add_argument(
        "filename", help="The filename of the contract or truffle directory to analyze."
    )
    parser.add_argument(
        "--verbose-test",
        "-v",
        help="verbose mode output for testing",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--verbose-json", "-j", help="verbose json output", action="store_true", default=False,
    )
    parser.add_argument(
        "--version", help="displays the current version", version="0.1.0", action="version",
    )

    parser.add_argument(
        "--config-file",
        help="Provide a config file (default: fortress.config.json)",
        action="store",
        dest="config_file",
        default="fortress.config.json",
    )

    group_detector = parser.add_argument_group("Detectors")
    group_detector.add_argument(
        "--detect",
        help="Comma-separated list of detectors, defaults to all, "
        "available detectors: {}".format(", ".join(d for d in available_detectors)),
        action="store",
        dest="detectors_to_run",
        default="all",
    )

    group_detector.add_argument(
        "--exclude",
        help="Comma-separated list of detectors to exclude,"
        "available detectors: {}".format(", ".join(d for d in available_detectors)),
        action="store",
        dest="detectors_to_exclude",
        default="all",
    )

    cryticparser.init(parser)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def main():
    # ------------------------------
    #       Usage: python3 -m fortress_format filename
    #       Example: python3 -m fortress_format contract.sol
    # ------------------------------
    # Parse all arguments
    args = parse_args()

    read_config_file(args)

    # Perform fortress analysis on the given filename
    fortress = Fortress(args.filename, **vars(args))

    # Format the input files based on fortress analysis
    fortress_format(fortress, **vars(args))


if __name__ == "__main__":
    main()
