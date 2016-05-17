# Bayes Net Implementation
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway

import networkx as nx

from itertools import product, combinations
from collections import Counter
from copy import deepcopy, copy
from abc import ABC, abstractmethod, ABCMeta

from warnings import warn

from utils import OrderedMultiDict


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

class Factor(object):
    def __init__(self, unconditioned_vars, conditioned_vars, variable_domains):
        self._domains = variable_domains
        self._variables = set(conditioned_vars) | set(unconditioned_vars)
        self._unconditioned = unconditioned_vars
        self._conditioned = conditioned_vars
        self.__entrees = product(*variable_domains.values())
        self._table = {entree: 3 for entree in entrees}

    def getProbability(self, variables):
        if hasattr(variables, __iter__):
            count_vars = Counter(variables)
            to_sum = [entree for entree in self.__entrees if Counter(entree) == count_vars]
            return sum(self._table[entree] for entree in to_sum)

        raise UserWarning("Error in retrieving probability. Invalid method call.")
        return 0

    def setProbability(self, variables, val):
        assert set(variables) ^ set(self._variables) == set(), "Variables for assignment not Valid for JPT"
        count_vars = Counter(variables)
        entrees = [entree for entree in self.__entrees if count_vars == Counter(entree)]
        if len(entrees) > 0:
            print("ERROR IN SET PROBABILITY JPT")
        entree = entrees[0]
        self._table[entree] = val


    def __str__(self):
        longest_var = max(map(len,self._variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({unc}{given}{cond})".format(unc=", ".join(self._unconditioned),
                                            given=" | ",
                                            cond=", ".join(self._conditioned))
        lst_of_entrees = [" | ".join(map(str_helper, k)) + " | " + str(v) for k, v in sorted(self._cpt.items())]
        table = "\n".join(lst_of_entrees)
        cpt_str = "{header}\n{rule}\n{table}".format(table=table, header=header, rule="-" * len(header))
        return cpt_str


class JPT(Factor):

    def __init__(self, variables, variable_domains):
        self._domains = variable_domains
        self._all_variables = variable_domains.keys()
        self._variables = set(variables)

        entree_temp = [[(var, domain) for domain in self._domains[var]] for var in self._variables]
        self.__entrees = list([element for element in product(*a)])
        # print(self.__entrees)
        self._table = OrderedMultiDict()


    def getEntrees(self):
        return self.__entrees

    def getProbability(self, variables):
        if isinstance(variables, str):
            var = variables
            to_sum = [entree for entree in self.__entrees if var in entree]
            return sum(self._table[entree] for entree in to_sum)
            # SUmm out
        if hasattr(variables, __iter__):
            count_vars = Counter(variables)
            to_sum = [entree for entree in self.__entrees if Counter(entree) == count_vars]
            return sum(self._table[entree] for entree in to_sum)
        raise UserWarning("Error in retrieving probability. Invalid method call.")
        return 0

    def setProbability(self, variables, val):
        print(variables)
        print(self._variables)
        assert set(variables) ^ set(self._variables) == set(), "Variables for assignment not Valid for JPT"
        count_vars = Counter(variables)
        entrees = [entree for entree in self.__entrees if count_vars == Counter(entree)]
        if len(entrees) > 0:
            print("ERROR IN SET PROBABILITY JPT")
        entree = entrees[0]
        self._table[entree] = val

    def __str__(self):
        longest_var = max(map(len,self._all_variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({vars})".format(vars=", ".join(self._variables))
        lst_of_entrees = [" | ".join(map(str_helper, k)) + " | " + str(v) for k, v in sorted(self._cpt.items())]
        table = "\n".join(lst_of_entrees)
        cpt_str = "{header}\n{rule}\n{table}".format(table=table, header=header, rule="-" * len(header))
        return cpt_str

class CPT(Factor):
    def __init__(self, unconditioned_var, conditioned_vars, variable_domains):
        self._domains = variable_domains
        self._variables = set(conditioned_vars) | set(unconditioned_var)
        self._unconditioned = unconditioned_var
        self._conditioned = conditioned_vars
        entrees = product(*variable_domains.values())
        self._cpt = {entree: 3 for entree in entrees}


    def __str__(self):
        longest_var = max(map(len,self._variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({unc} | {cond})".format(unc=self._unconditioned,
                                            cond=", ".join(self._conditioned))
        lst_of_entrees = [" | ".join(map(str_helper, k)) + " | " + str(v) for k, v in sorted(self._cpt.items())]
        table = "\n".join(lst_of_entrees)
        cpt_str = "{header}\n{rule}\n{table}".format(table=table, header=header, rule="-" * len(header))
        return cpt_str

# AbstractProbabilityTable.register(CPT)
# AbstractProbabilityTable.register(JPT)
# AbstractProbabilityTable.register(Factor)

variableDomains = {"weather": ["sun", "rain"], "forecast": ["good", "bad"]}
variables = variableDomains.keys()
# b = BayesNet([("weather", "forecast")], variables, variableDomains)
jpt = JPT(variables, variableDomains)
entrees = jpt.getEntrees()
# print(entrees)
# # print(list(entrees))
# for entree in list(entrees):
#     jpt.setProbability(entrees, .1)
