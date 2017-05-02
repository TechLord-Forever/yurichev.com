#!/usr/bin/python

# new: printing unsat core.

from z3 import *
import sys, re

# MS Excel or LibreOffice style.
# first top-left cell is A0, not A1
def coord_to_name(R, C):        
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[R]+str(C)

# open file and parse it as list of lists:
f=open(sys.argv[1],"r")
# filter(None, ...) to remove empty sublists:
ar=filter(None, [item.rstrip().split() for item in f.readlines()])
f.close()

WIDTH=len(ar[0])
HEIGHT=len(ar)

# cells{} is a dictionary with keys like "A0", "B9", etc:
cells={}
for R in range(HEIGHT):
    for C in range(WIDTH):
        name=coord_to_name(R, C)
        cells[name]=Int(name)

s=Solver()
s.set(unsat_core=True)

cur_R=0
cur_C=0

for row in ar:
    for c in row:
        # string like "A0+B2" becomes "cells["A0"]+cells["B2"]":
        c=re.sub(r'([A-Z]{1}[0-9]+)', r'cells["\1"]', c)
        st="cells[\"%s\"]==%s" % (coord_to_name(cur_R, cur_C), c)
        # evaluate string. Z3Py expression is constructed at this step:
        e=eval(st)
        # add constraint:
        s.assert_and_track(e, coord_to_name(cur_R, cur_C))
        cur_C=cur_C+1
    cur_R=cur_R+1
    cur_C=0

result=str(s.check())
print result
if result=="sat":
    m=s.model()
    for r in range(HEIGHT):
        for c in range(WIDTH):
            sys.stdout.write (str(m[cells[coord_to_name(r, c)]])+"\t")
        sys.stdout.write ("\n")
else:
    print s.unsat_core()

