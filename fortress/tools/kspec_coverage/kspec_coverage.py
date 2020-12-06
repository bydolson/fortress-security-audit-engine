from fortress.tools.kspec_coverage.analysis import run_analysis
from fortress import Fortress


def kspec_coverage(args):

    contract = args.contract
    kspec = args.kspec

    fortress = Fortress(contract, **vars(args))

    # Run the analysis on the Klab specs
    run_analysis(args, fortress, kspec)
