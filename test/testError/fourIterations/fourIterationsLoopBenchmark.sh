#!/bin/bash

# This benchmark is used in fourIterationsErrorTest.sh.

IMAGES="Pharo11"
VMs="latest10"

# This command only fails if ITERATION is odd, so that with 4 iterations, it fails one in two times.
# In errorTest it is checked that the iterations indeed failed one in two times
PHARO_CMD='eval ($ITERATION \\ 2) == 0 ifFalse: [ self error ]'

runBenchs