#!/usr/bin/env python3

import json
from sys import argv

# read input
with open(argv[1]) as fo:
  data = {}
  for line in fo.readlines():
    elems = line.strip().split(",")
    if len(elems)!=3: next
    
    algo =       elems[0]
    n    =   int(elems[1])
    t    = float(elems[2])
    
    if not algo in data: data[algo] = {}
    data[algo][n] = t

# find algo, ns, and min and max cell value
algos = []
ns = []
mn = mx = None
for algo in data.keys():
  for n in data[algo]:
    if not algo in algos: algos.append(algo)
    if not n in ns: ns.append(n)
    
    value = data[algo][n]
    if mn==None or value<mn: mn = value
    if mx==None or value>mx: mx = value

valuemapper = lambda v: (float(v)-mn)/(mx-mn)*100

xcount = len(ns)
ycount = len(algos)

# produce result
yheading = "\\multirow{%i}{*}{\\rotatebox{90}{\\centering Algorithm}}" % ycount
lines = []
lines.append("\\begin{tabular}{rl%s}" % ("c"*xcount))
lines.append("  & & \\multicolumn{%i}{c}{Number of Operations / [in 1,000,000]} \\\\" % xcount)
lines.append("  & "+("".join(map(lambda key: " & "+str(int(key/1000000)), ns)))+" \\\\")
for algo in algos:
  line = "  %s & %s" % (yheading if algo==algos[0] else "", algo)
  for n in sorted(ns):
    value = data[algo][n]
    line += " &\\cellcolor{red!%i!green}%.2f" % (valuemapper(value), value)
  lines.append(line+" \\\\")
lines.append("\\end{tabular}")

# write output
with open(argv[2], "w") as fo:
  fo.writelines("".join(map(lambda line: line+"\n", lines)))
