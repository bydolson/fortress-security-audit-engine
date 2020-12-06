#!/usr/bin/env bash

### Test fortress-prop

cd examples/fortress-prop || exit 1
fortress-prop . --contract ERC20Buggy
if [ ! -f contracts/crytic/TestERC20BuggyTransferable.sol ]; then
    echo "fortress-prop failed"
    return 1
fi
