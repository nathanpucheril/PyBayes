# Bayes Net Implementation
# ________________________
# @author Nathan Pucheril 
# @author Keith Hardaway

import networkx
from itertools import product


class BayesNet(object):
    """docstring for """
    def __init__(self, variables, domains, cpts={}, title="Bayes Net"):
        self._variables = variables
        self._variable_domains = domains
        self._cpts = cpts
        self._title = title

    @property
    def variables(self):
        return self._variables

    @property
    def variableDomains(self):
        return self._variable_domains

    @property
    def cpts(self):
        return self._cpts

    def getCPT(self, variable):
        return self._cpts[variable]

    def setCPT(self, variable, cpt):
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
        net_str = ("*{title} {class_}*\n"
                   "Variables: {variables}\n"
                   "Variable Domains:\n\t\t{domains}\n"
                   "CPTS: {cpt_str}\n{border}\n"
                   ).format(title = self._title,
                            class_ = self.__class__, \
                            variables = "; ".join(map(str, self._variables)),
                            domains = '\n\t\t'.join(["{k} :: {v}".format(k=k.ljust(LJUSTVAL, " "), v=v) for k, v in self._variable_domains.items()]),
                            cpt_str = cpt_str,
                            border = "*" * 80)

        return net_str




class SimpleBayesNet(BayesNet):
    pass

class DecisionNetwork(BayesNet):
    pass


class Sampler(object):
    pass

class ProbabilityTable(object):


class Factor(ProbabilityTable):
    pass

class CPT(ProbabilityTable):
    def __init__(self, variable_domains, unconditioned_vars, conditioned_vars = {}):
        self._domains = variable_domains
        self._all_variables = variable_domains.keys()
        self._unconditioned = unconditioned_vars
        self._conditioned = conditioned_vars
        entrees = product(*variable_domains.values())
        self._cpt = {entree: 3 for entree in entrees}

    def getProbability(self, entree):
        return self._cpt[entree]

    def setProbability(self, entree, val):
        self._cpt[entree] = val


    def __str__(self):
        longest_var = max(map(len,self._all_variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({unc}{given}{cond})".format(unc=", ".join(self._unconditioned),
                                                cond=", ".join(self._conditioned),
                                                given=" | " if self._conditioned else "")
        lst_of_entrees = [" | ".join(map(str_helper, k)) + " | " + str(v) for k, v in sorted(self._cpt.items())]
        table = "\n".join(lst_of_entrees)
        cpt_str = "{header}\n{rule}\n{table}".format(table=table, header=header, rule="-" * len(header))
        return cpt_str

# print("*" * 100)
variableDomains = {"weather": ["sun", "rain"], "forecast": ["good", "bad"]}
variables = variableDomains.keys()
b = BayesNet(variables, variableDomains)
print(b)
p = product(*variableDomains.values())
c = CPT(variableDomains, variables)
# c.setProbability()
print(c)
