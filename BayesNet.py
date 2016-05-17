# Bayes Net Implementation
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway

import networkx as nx

from copy import deepcopy, copy
# from abc import ABC, abstractmethod, ABCMeta

from ProbabilityTable import *
# from utils import Unorder edMultiDict


class BayesNet(object):
    """docstring for """
    def __init__(self, edges, variables, domains, probability_tables={}, title="Bayes Net"):
        self._edges = edges
        self._variables = variables
        self._variable_domains = domains
        self._tables = probability_tables
        self._title = title

        assert all([(u in variables and v in variables) for u, v in edges]),"h"
        assert isinstance(self._tables, dict), "Probability Tables must be a Dictionary"
        assert all([isinstance(table, Factor) for table in self._tables]), "Tables must be of type Factor"
        if self._tables == {}:
            warnings.warn("Probability Tables Undefined")
        elif set(self._tables.keys()) - set(self._variables) == set():
            warnings.warn("Not all Probability Tables Defined")
    @property
    def variables(self):
        return copy(self._variables)

    @property
    def variableDomains(self):
        return deepcopy(self._variable_domains)

    @property
    def tables(self):
        return self._tables

    def getProbabilityTable(self, variable):
        return self._tables[variable]

    def setProbabilityTable(self, variable, cpt):
        pass

    def __eq__(self, object2):
        return self.variables == object2.variables and  \
            self.variableDomains == object2.variableDomains and \
            self.cpts == object2.cpts

    def __ne__(self, object2):
        return not self.__eq__(object2)

    def __str__(self):
        cpt_str = ""
        LJUSTVAL = 10
        domain_str = '\n\t\t'.join(["{k} :: {v}".format(k=k.ljust(LJUSTVAL, " "), v=v) for k, v in self._variable_domains.items()])
        net_str = ("*{title} {class_}*\n"
                   "Variables: {variables}\n"
                   "Variable Domains:\n\t\t{domains}\n"
                   "CPTS: {cpt_str}\n{border}\n"
                   ).format(title = self._title,
                            class_ = self.__class__, \
                            variables = "; ".join(map(str, self._variables)),
                            domains = domain_str,
                            border = "*" * 80)

        return net_str

    def loadable_string(self):
        return "{edges}\n{vars}\n{domains}\n{tables}\n{title}".format(
        edges = self._edges,
        vars = self._variables,
        domains = self._variable_domains,
        tables = self._tables,
        title = self._title,
        )
    def visual_graph(self):
        import matplotlib.pyplot as plt
        net = nx.DiGraph()
        # print("h")
        net.add_nodes_from(self._variables)
        net.add_edges_from(self._edges)
        nx.draw(net)
        plt.show()

    @staticmethod
    def load_bayes_net(bayes_str):
        return BayesNet(None, None, None, None)
#     def save_graph(self):
#         nx.draw(G)
# >>> plt.savefig("path.png")

class DecisionNetwork(BayesNet):
    pass

#
# class AbstractProbabilityTable(metaclass=ABCMeta):
#
#     __metaclass__ = ABCMeta
#
#     @abstractmethod
#     def __init__(self, variables, variable_domains):
#         self._table = {}
#         self._domains = variable_domains
#         self._all_variables = variable_domains.keys()
#         self._variables = variables
#
#     def getProbability(self, entree):
#         return self._table[entree]
#
#     def setProbability(self, entree, val):
#         self._table[entree] = val
#



variableDomains = {"weather": ["sun", "rain"], "forecast": ["good", "bad"]}
variables = variableDomains.keys()
# b = BayesNet([("weather", "forecast")], variables, variableDomains)
jpt = JPT(variables, variableDomains)
entrees = jpt.getEntrees()
# print("\n".join(map(str, entrees)))
print(jpt.get_probability(weather = "sun", forecast = "good"))
print(jpt.set_probability(41, weather = "sun", forecast = "good"))
print(jpt.get_probability(weather = "sun", forecast = "good"))
print(jpt)
# print(entrees)
# # print(list(entrees))
# for entree in list(entrees):
#     jpt.setProbability(entrees, .1)
