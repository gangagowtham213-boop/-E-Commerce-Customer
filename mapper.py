#!/usr/bin/env python3
import sys, csv
for row in csv.reader(sys.stdin):
    if len(row) < 8 or row[0].lower() == "invoiceno": continue
    invoice, stock, desc, qty, dt, price, customer, country = row[:8]
    try:
        q=float(qty); p=float(price)
        if invoice.upper().startswith("C") or q<=0 or p<=0: continue
        print(f"{country}\t{q*p}")
    except: pass
