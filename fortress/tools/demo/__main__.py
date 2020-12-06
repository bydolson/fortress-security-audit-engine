import argparse
import logging
from crytic_compile import cryticparser
from fortress import Fortress

logging.basicConfig()
logging.getLogger("Fortress").setLevel(logging.INFO)

logger = logging.getLogger("Fortress-demo")


def parse_args():
    """
    Parse the underlying arguments for the program.
    :return: Returns the arguments for the program.
    """
    parser = argparse.ArgumentParser(description="Demo", usage="fortress-demo filename")

    parser.add_argument(
        "filename", help="The filename of the contract or truffle directory to analyze."
    )

    # Add default arguments from crytic-compile
    cryticparser.init(parser)

    return parser.parse_args()


def main():
    args = parse_args()

    # Perform fortress analysis on the given filename
    _fortress = Fortress(args.filename, **vars(args))

    logger.info("Analysis done!")


if __name__ == "__main__":
    main()
