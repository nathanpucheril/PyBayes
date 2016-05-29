import pytest

from PyBayes.BayesNet import BayesNet
from PyBayes.ProbabilityTable import *

class TestValidNet:
    def test_one(self):
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
        assert bn.is_valid() == True

    def test_two(self):
        edges = [('x', 'y')]
        variables = ['x', 'y']
        domains = {'x': (0,1), 'y': (0,1)}
        xcpt = CPT('x', (), domains)
        xcpt.set_probability(.4, x=0)
        xcpt.set_probability(.6, x=1)

        ycpt = CPT('y', (), {'y': (0, 1)})
        ycpt.set_probability(.3, y=0)
        ycpt.set_probability(.7, y=1)
        cptDict = {'x': xcpt, 'y': ycpt}
        bn = BayesNet(edges, variables, domains, cptDict)
        assert bn.is_valid() == False

    def test_three(self):
        edges = [('x', 'y'), ('x', 'z')]
        variables = ['x', 'y', 'z']
        domains = {'x': (0,1), 'y': (0,1), 'z':(0,1)}
        zcpt = CPT('z', (), domains)
        zcpt.set_probability(.5, z=0)
        zcpt.set_probability(.5, z=1)

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
        assert bn.is_valid() == False
