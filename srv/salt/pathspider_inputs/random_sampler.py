#!/usr/bin/env python3

import sys
import random

FIXED_NUMBER_FROM_TOP = 1000
TOTAL_NUMBER_OF_ENTRIES = 10000
LOWER_SELECTION_BOUND = 100000

input_file = open(sys.argv[1])
output_file = open(sys.argv[2], 'w')

selected = list(range(0, FIXED_NUMBER_FROM_TOP))
candidates = set(range(FIXED_NUMBER_FROM_TOP, LOWER_SELECTION_BOUND))
number_to_select = TOTAL_NUMBER_OF_ENTRIES - FIXED_NUMBER_FROM_TOP

selected = selected + random.sample(candidates, number_to_select)
selected.sort()

last_line = 0
for line in selected:
    delta = line - last_line

    # seek
    for i in range(delta):
        input_file.readline()

    # copy line to output
    output_file.write(input_file.readline())

    last_line = line

