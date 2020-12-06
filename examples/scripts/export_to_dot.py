import sys
from fortress.fortress import Fortress


if len(sys.argv) != 2:
    print("python function_called.py contract.sol")
    sys.exit(-1)

# Init fortress
fortress = Fortress(sys.argv[1])

for contract in fortress.contracts:
    for function in contract.functions + contract.modifiers:
        filename = "{}-{}-{}.dot".format(sys.argv[1], contract.name, function.full_name)
        print("Export {}".format(filename))
        function.slithir_cfg_to_dot(filename)
