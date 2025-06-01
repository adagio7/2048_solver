#!/bin/bash

python3 -m src.solvers.genetic \
    --population-size 50 \
    --generations 30 \
    --mutation-rate 0.2 \
    --elite-size 10 \
    --save-results \
        --output-file "heuristic_weights.json"
