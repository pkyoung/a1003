#!/opt/conda/bin/python

import sys
import os

for line in open(sys.argv[1]):
    line = line.strip()
    basename = os.path.basename(line)
    key = os.path.splitext(basename)[0]
    txtfname = os.path.splitext(line)[0] + ".txt"
    transcript = open(txtfname).readline().strip()
    print(key, transcript)
