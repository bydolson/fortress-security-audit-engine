from fortress.detectors.abstract_detector import AbstractDetector, DetectorClassification


class Backdoor(AbstractDetector):
    """
    Detect function named backdoor
    """

    ARGUMENT = "backdoor"  # fortress will launch the detector with fortress.py --mydetector
    HELP = "Function named backdoor (detector example)"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/trailofbits/fortress/wiki/Adding-a-new-detector"
    WIKI_TITLE = "Backdoor example"
    WIKI_DESCRIPTION = "Plugin example"
    WIKI_EXPLOIT_SCENARIO = ".."
    WIKI_RECOMMENDATION = ".."

    def _detect(self):
        results = []

        for contract in self.fortress.contracts_derived:
            # Check if a function has 'backdoor' in its name
            for f in contract.functions:
                if "backdoor" in f.name:
                    # Info to be printed
                    info = ["Backdoor function found in ", f, "\n"]

                    # Add the result in result
                    res = self.generate_result(info)

                    results.append(res)

        return results
