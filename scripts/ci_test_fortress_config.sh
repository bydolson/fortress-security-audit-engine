#!/usr/bin/env bash

### Test

if ! fortress "tests/*.json" --config "tests/config/fortress.config.json"; then
    echo "Config failed"
    exit 1
fi

