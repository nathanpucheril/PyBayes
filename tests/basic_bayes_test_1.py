from PyBayes.BayesNet import BayesNet
from PyBayes.ProbabilityTable import *

edges = [('x', 'y')]
variables = ['x', 'y']
domains = {'x': (0,1), 'y': (0,1)}
xcpt = CPT('x', ('y'), domains)
xcpt.set_probability(.7, x=0, y=1)
xcpt.set_probability(.3, x=0, y=0)
xcpt.set_probability(.2, x=1, y=1)
xcpt.set_probability(.8, x=1, y=0)

ycpt = CPT('y', (), {'y': (0, 1)})
ycpt.set_probability(.3, y=0)
ycpt.set_probability(.7, y=1)
cptDict = {'x': xcpt, 'y': ycpt}
bn = BayesNet(edges, variables, domains, cptDict)

print(bn)
