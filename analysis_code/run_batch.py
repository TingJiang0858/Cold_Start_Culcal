#!/usr/bin/env python3

from __future__ import print_function
import subprocess
import os
from pprint import pprint
import sys
import random

def main(argv):

    for interval in argv:
        print ("\n\nrun calculating cold start with time interval of", interval)
        os.system ("python3 cal_cold_start.py '%s'" % interval)

    print ("Done...")

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
