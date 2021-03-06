#!/usr/bin/env bash

### Test printer

# Needed for evm printer
pip install evm-cfg-builder

if ! fortress "tests/*.json" --print all --json -; then
    echo "Printer tests failed"
    exit 1
fi

solc use "0.5.1"

fortress examples/scripts/test_evm_api.sol --print evm
