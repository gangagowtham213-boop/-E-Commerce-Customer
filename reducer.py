#!/usr/bin/env python3
import sys
current=None; total=0.0
for line in sys.stdin:
    key, value = line.rstrip("\n").split("\t",1)
    if current is not None and key != current:
        print(f"{current}\t{total:.2f}")
        total=0.0
    current=key; total += float(value)
if current is not None: print(f"{current}\t{total:.2f}")
