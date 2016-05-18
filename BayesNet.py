# Bayes Net Implementation
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway

import networkx as nx

from copy import deepcopy, copy

from ProbabilityTable import *


class BayesNet(object):
    """ Bayes Net Implementation

        Usage:
            -
            -
            -
            -
    """
    def __init__(self, edges, variables, domains, probability_tables={}, title="Bayes Net"):
        self._edges = edges
        self._variables = variables
        self._variable_domains = domains
        self._cpts = probability_tables
        self._title = title
        self._jpt = None

        assert all([(u in variables and v in variables) for u, v in edges]),"h"
        assert isinstance(self._cpts, dict), "Probability Tables must be a Dictionary of CPTS"
        assert all([isinstance(table, CPT) for table in self._cpts]), "Tables must be of type CPT"
        if self._cpts == {}:
            warnings.warn("Probability Tables Undefined")
        elif set(self._cpts.keys()) - set(self._variables) == set():
            warnings.warn("Not all Probability Tables Defined")

    @property
    def variables(self):
        return copy(self._variables)

    @property
    def variable_domains(self):
        return deepcopy(self._variable_domains)

    @property
    def cpts(self):
        return self._cpts

    def get_jpt(self):
        if self._jpt:
            return self._jpt
        self._jpt = Factor.cpts2jpt(self._cpts)
        return self._jpt

    def get_cpt(self, variable):
        """ Gets probability table of a particular variable"""
        return self._tables[variable]

    def set_cpt(self, variable, cpt):
        """ Sets probability table of a particular variable"""
        assert isinstance(cpt, CPT), "Bayes Net use Conditional Probability Tables"
        self._tables[variable] = cpt


    def __eq__(self, object2):
        """ Checks for Bayes Net Equality. Not CPT Equality!"""
        return self.variables == object2.variables and  \
            self.variableDomains == object2.variableDomains and \
            self.cpts == object2.cpts

    def __ne__(self, object2):
        """ Checks for non-equality"""
        return not self.__eq__(object2)

    def __str__(self):
        """Human readable Bayes Net String """
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
        """ String for loading a bayes net"""
        return "{edges}\n{vars}\n{domains}\n{tables}\n{title}".format(
                edges = self._edges,
                vars = self._variables,
                domains = self._variable_domains,
                tables = self._tables,
                title = self._title,
                )

    def visual_graph(self):
        """ Network x image of Bayes Net with Directed Edges"""
        import matplotlib.pyplot as plt
        net = nx.DiGraph()
        # print("h")
        net.add_nodes_from(self._variables)
        net.add_edges_from(self._edges)
        nx.draw(net)
        plt.show()

    @staticmethod
    def load_bayes_net(bayes_str):
        """ Loads BayesNet from Bayes Net Loadable String.
            See method loadable_string(self)
        """
        return BayesNet(None, None, None, None)

#     def save_graph(self):
#         nx.draw(G)
# >>> plt.savefig("path.png")



class DecisionNetwork(BayesNet):
    def get_utility():
        pass
    def VPI():
        pass

class HMM(BayesNet):
    def time_elapse(self):
        pass
    def observe(self):
        pass



def BayesNetConstructor():
    pass

def HMMConstructor():
    pass

def DecisionNetworkConstructor():
    pass
