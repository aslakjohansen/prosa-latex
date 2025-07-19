#!/usr/bin/env python3

from time import perf_counter

def report(algo, n, time):
  print(",".join([algo, str(n), str(time)]))

def run_list(n):
  l = []
  for i in range(n):
    l.append(i)

def run_dict(n):
  d = {}
  for i in range(n):
    d[i] = [i]

algos = {
  "list append": run_list,
  "dict insert": run_dict,
}

for algo in ["list append", "dict insert"]:
  for i in [4, 8, 12, 16, 20, 24, 28, 32, 36, 40]:
    n = i * 1000 * 1000
    fun = algos[algo]
    t0 = perf_counter()
    fun(n)
    t1 = perf_counter()
    report(algo, n, t1-t0)
