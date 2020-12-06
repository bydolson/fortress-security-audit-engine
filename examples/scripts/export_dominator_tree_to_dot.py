import sys
from fortress.fortress import Fortress


if len(sys.argv) != 2:
    print("python export_dominator_tree_to_dot.py contract.sol")
    sys.exit(-1)

# Init fortress
fortress = Fortress(sys.argv[1])

for contract in fortress.contracts:
    for function in list(contract.functions) + list(contract.modifiers):
        filename = "{}-{}-{}_dom.dot".format(sys.argv[1], contract.name, function.full_name)
        print("Export {}".format(filename))
        function.dominator_tree_to_dot(filename)
