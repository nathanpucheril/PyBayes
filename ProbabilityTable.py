# Probability Tables Implementation
# ---------------------------------
# @author Nathan Pucheril
# @author Keith Hardaway

from itertools import product, combinations
from copy import deepcopy, copy
from warnings import warn
from functools import reduce

class Factor(object):
    """ Description:
        Usage:
            -
            -
            -
    """

    def __init__(self, unconditioned_vars, conditioned_vars, variable_domains):
        """ Creates a Factor object that encodes probabilities in a table """
        self._domains = variable_domains
        self._variables = set(conditioned_vars) | set(unconditioned_vars)
        self._unconditioned = unconditioned_vars
        self._conditioned = conditioned_vars
        entry_temp = [[(var, domain) for domain in self._domains[var]] for var in self._variables]
        self._entries = list(sorted(product(*entry_temp)))
        self._table = {}
        for entry in self._entries:
            self._table[entry] = 0
        warn("Probabilities not set. Default = 0")

    def get_entries(self):
        """ Retrieves all possible entries to the table"""
        return self._entries

    def get_probability(self, **variables):
        """ Gets probability of a specific entry in table"""
    def get_domains(self):
        return deepcopy(self._domains)

    def get_probability(self, **variables):
        """ Gets probability of a specific entree in table """
        variables = variables.items()
        if hasattr(variables, "__iter__"):
            to_sum = [entry for entry in self._entries if set(entry) == set(variables)]
            if len(to_sum) != 1:
                raise UserWarning("Error in retrieving probability. Invalid method call.")
            return self._table[to_sum[0]]
        raise UserWarning("Error in retrieving probability. Invalid method call.")
        return 0

    def set_probability(self, val, **variables):
        """ Sets probability of a specific entry in table"""
        assert set(variables) ^ set(self._variables) == set(), "Variables for assignment not Valid for JPT"
        variables = variables.items()
        entries = [entry for entry in self._entries if set(entry) | set(variables) == set(entry)]
        if len(entries) > 1:
            print("ERROR IN SET PROBABILITY JPT")
        else:
            entry = entries[0]
            self._table[entry] = val


    def __str__(self):
        """ Returns human readable Probability Table """
        longest_var = max(map(len,self._variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({unc}{given}{cond})".format(unc=", ".join(self._unconditioned),
                                            given=" | " if self._conditioned else "",
                                            cond=", ".join(self._conditioned))
        var_header = str_helper("{vars}".format(vars=" | ".join(self._variables)))
        lst_of_entries = [" | ".join(map(str_helper, map(lambda x: x[1], k))) + " | " + str(v) for k, v in sorted(self._table.items())]
        table = "\n".join(lst_of_entries)
        return "{header}\n{rule}\n{var_header}\n{table}".format(table=table,
            header=header, var_header = var_header, rule="-" * len(header))

    def load_factor(self, string):
        pass

    def loadable_string(self):
        pass

class JPT(Factor):

    def __init__(self, variables, variable_domains):
        """Initializes a Joint Probability Table """
        super().__init__(variables, set(), variable_domains)

    def valid_table(self):
        """Checks if Probability Rules are followed"""
        assert sum(self._table[entry] for entry in self.get_entries()) == 1, "JPT does not sum to 1"
        return True if sum(self._table[entry] for entry in self.get_entries()) == 1 else False

    def get_probability(self, **variables):
        """ Gets probability of certain variables. Includes summing out over vars """
        # variables = variables.items()
        if len(variables) == 1:
            var = tuple(list(variables.items())[0])
            to_sum = [entry for entry in self._entries if var in entry]
            return sum(self._table[entry] for entry in to_sum)
        return super().get_probability(**variables)

class CPT(Factor):
    def __init__(self, unconditioned_var, conditioned_vars, variable_domains):
        super().__init__(list([unconditioned_var]), list([conditioned_vars]), variable_domains)

    @staticmethod
    def cpts2jpt(cpts):
        """Converts mutliple CPTs to JPT """
        all_domains = {}
        for cpt in cpts:
            all_domains.update(cpt.get_domains())
        jpt = JPT(all_domains.keys(), all_domains)
        jpt_entrees = jpt.get_entrees()
        for entree in jpt_entrees:
            prob = 1
            for cpt in cpts:
                for cpt_entree in cpt.get_entrees():
                    if set(cpt_entree) | set(entree) == set(entree): # Union of CPT and JPT does not yield new Vars
                        prob *= cpt.get_probability(**dict(cpt_entree)) #shouldnt have to put entree in dict
            jpt.set_probability(prob, **dict(entree))#shouldnt have to put entree in dict
        return jpt




def variable_elimination(elimination_var, factors):
    pass

# var1 = ["hi", "bye"]
# dom1 = {"hi": ["friend", "parent"], "bye": ["friend", "parent"]}
# var2 = ["mom", "dad"]
# dom2 = {"mom": ["scold", "praise"], "dad": ["scold", "praise"]}
#
# cpt1 = CPT("hi", "bye", dom1)
# entrees = cpt1.get_entrees()
# # print(entrees)
# for entree in entrees:
#     # print(dict(entree))
#     cpt1.set_probability(.2, **dict(entree))
#
# cpt2 = CPT("mom", "dad", dom2)
# entrees = cpt2.get_entrees()
# # print(entrees)
# for entree in entrees:
#     # print(dict(entree))
#     cpt2.set_probability(.1, **dict(entree))
#
# print(cpt1)
# print(cpt2)
#
# jpt = CPT.cpts2jpt([cpt1, cpt2])
# print(jpt)
