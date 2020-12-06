import sys

from fortress.core.declarations.solidity_variables import SolidityVariableComposed
from fortress.core.variables.state_variable import StateVariable
from fortress.fortress import Fortress
from fortress.slithir.operations.high_level_call import HighLevelCall
from fortress.slithir.operations.index import Index
from fortress.slithir.variables.reference import ReferenceVariable
from fortress.slithir.variables.temporary import TemporaryVariable


def visit_node(node, visited):
    if node in visited:
        return

    visited += [node]
    taints = node.function.fortress.context[KEY]

    refs = {}
    for ir in node.irs:
        if isinstance(ir, Index):
            refs[ir.lvalue] = ir.variable_left

        if isinstance(ir, Index):
            read = [ir.variable_left]
        else:
            read = ir.read
        print(ir)
        print("Refs {}".format(refs))
        print("Read {}".format([str(x) for x in ir.read]))
        print("Before {}".format([str(x) for x in taints]))
        if any(var_read in taints for var_read in read):
            taints += [ir.lvalue]
            lvalue = ir.lvalue
            while isinstance(lvalue, ReferenceVariable):
                taints += [refs[lvalue]]
                lvalue = refs[lvalue]

        print("After {}".format([str(x) for x in taints]))
        print()

    taints = [v for v in taints if not isinstance(v, (TemporaryVariable, ReferenceVariable))]

    node.function.fortress.context[KEY] = list(set(taints))

    for son in node.sons:
        visit_node(son, visited)


def check_call(func, taints):
    for node in func.nodes:
        for ir in node.irs:
            if isinstance(ir, HighLevelCall):
                if ir.destination in taints:
                    print("Call to tainted address found in {}".format(function.name))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python taint_mapping.py taint.sol")
        sys.exit(-1)

    # Init fortress
    fortress = Fortress(sys.argv[1])

    initial_taint = [SolidityVariableComposed("msg.sender")]
    initial_taint += [SolidityVariableComposed("msg.value")]

    KEY = "TAINT"

    prev_taints = []
    fortress.context[KEY] = initial_taint
    while set(prev_taints) != set(fortress.context[KEY]):
        prev_taints = fortress.context[KEY]
        for contract in fortress.contracts:
            for function in contract.functions:
                print("Function {}".format(function.name))
                fortress.context[KEY] = list(set(fortress.context[KEY] + function.parameters))
                visit_node(function.entry_point, [])
                print("All variables tainted : {}".format([str(v) for v in fortress.context[KEY]]))

            for function in contract.functions:
                check_call(function, fortress.context[KEY])

    print(
        "All state variables tainted : {}".format(
            [str(v) for v in prev_taints if isinstance(v, StateVariable)]
        )
    )
