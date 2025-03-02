
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverFactory

import sys
import os

os.system("clear")

#sys.exit("Stopped")

Model = ConcreteModel()

# SETS & PARAMETERS********************************************************************
numNodes=5

N=RangeSet(1, numNodes)

cost={(1,1):999, (1,2):5,   (1,3):2,   (1,4):999, (1,5):999,\
      (2,1):999, (2,2):999, (2,3):999, (2,4):999, (2,5):8,\
      (3,1):999, (3,2):999, (3,3):999, (3,4):3,   (3,5):999,\
      (4,1):999, (4,2):999, (4,3):999, (4,4):999, (4,5):2,\
      (5,1):999, (5,2):999, (5,3):999, (5,4):999, (5,5):999}

# VARIABLES****************************************************************************
Model.x = Var(N,N, domain=Binary)

# OBJECTIVE FUNCTION*******************************************************************
Model.obj = Objective(expr = sum(Model.x[i,j]*cost[i,j] for i in N for j in N))

# CONSTRAINTS**************************************************************************
Model.res1=ConstraintList()
for i in N:
    if i==1:
        Model.res1.add(sum(Model.x[i,j] for j in N)==1)

Model.res2=ConstraintList()
for j in N:
    if j==5:
        Model.res2.add(sum(Model.x[i,j] for i in N)==1)

Model.res3=ConstraintList()
for i in N:
    if i!=1 and i!=5:
        Model.res3.add(sum(Model.x[i,j] for j in N) - sum(Model.x[j,i] for j in N)==0)
    
# APPLYING THE SOLVER******************************************************************
SolverFactory('glpk').solve(Model)

Model.display()



