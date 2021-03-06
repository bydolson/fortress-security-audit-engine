#!/usr/bin/env bash

### Test fortress-check-upgradability

DIR_TESTS="tests/possible_paths"

solc use "0.5.0"
fortress-find-paths "$DIR_TESTS/paths.sol"  A.destination  > test_possible_paths.txt 2>&1
DIFF=$(diff test_possible_paths.txt "$DIR_TESTS/paths.txt")
if [  "$DIFF" != "" ]
then
    echo "fortress-find-paths failed"
    cat test_possible_paths.txt
    cat "$DIR_TESTS/paths.txt"
    exit 255
fi
rm test_possible_paths.txt
