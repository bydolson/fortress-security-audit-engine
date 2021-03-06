from fortress.core.cfg.node import NodeType
from fortress.formatters.utils.patches import create_patch
from fortress.tools.mutator.mutators.abstract_mutator import AbstractMutator, FaultNature, FaulClass


class MIA(AbstractMutator):  # pylint: disable=too-few-public-methods
    NAME = "MIA"
    HELP = '"if" construct around statement'
    FAULTCLASS = FaulClass.Checking
    FAULTNATURE = FaultNature.Missing

    def _mutate(self):

        result = dict()

        for contract in self.fortress.contracts:

            for function in contract.functions_declared + contract.modifiers_declared:

                for node in function.nodes:
                    if node.type == NodeType.IF:
                        # Retrieve the file
                        in_file = contract.source_mapping["filename_absolute"]
                        # Retrieve the source code
                        in_file_str = contract.fortress.source_code[in_file]

                        # Get the string
                        start = node.source_mapping["start"]
                        stop = start + node.source_mapping["length"]
                        old_str = in_file_str[start:stop]

                        # Replace the expression with true
                        new_str = "true"

                        create_patch(result, in_file, start, stop, old_str, new_str)

        return result
