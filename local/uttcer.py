#!/usr/bin/env python3

import editdistance
import sys

ref = {}
hyp = {}
for line in open(sys.argv[1], "r"):
    key, *text = line.split()
    ref[key] = list(''.join(text))

for line in open(sys.argv[2], "r"):
    key, *text = line.split()
    hyp[key] = list(''.join(text))


N, E = 0, 0
for key in hyp:
    if key not in ref:
        raise Exception("no key '%s' in ref '%s'" %(key, sys.argv[1]))

    e = editdistance.eval(ref[key], hyp[key])
    n = len(ref[key])
    print(key, "%5.2f"%(e/n*100), e, n)

    N += n
    E += e

print("N= %d E= %d CER= %5.2f" %(N, E, E/N*100), file=sys.stderr)
