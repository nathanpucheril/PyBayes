# Probability Tables Implementation
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway

from itertools import product, combinations
from copy import deepcopy, copy
from warnings import warn

class Factor(object):
    """ Description:
        Usage:
            -
            -
            -
    """

    def __init__(self, unconditioned_vars, conditioned_vars, variable_domains):
        """ Creates a Factor object that encodes probabilities in a table"""
        self._domains = variable_domains
        self._variables = set(conditioned_vars) | set(unconditioned_vars)
        self._unconditioned = unconditioned_vars
        self._conditioned = conditioned_vars
        entry_temp = [[(var, domain) for domain in self._domains[var]] for var in self._variables]
        self._entrys = list(sorted(product(*entry_temp)))
        self._table = {}
        for entry in self._entrys:
            self._table[entry] = 0
        warn("Probabilities not set. Default = 0")

    def get_entrys(self):
        """ Retrieves all possible entrys to the table"""
        return self._entrys

    def get_probability(self, **variables):
        """ Gets probability of a specific entry in table"""
        variables = variables.items()
        if hasattr(variables, "__iter__"):
            to_sum = [entry for entry in self._entrys if set(entry) == set(variables)]
            if len(to_sum) != 1:
                raise UserWarning("Error in retrieving probability. Invalid method call.")
            return self._table[to_sum[0]]
        raise UserWarning("Error in retrieving probability. Invalid method call.")
        return 0

    def set_probability(self, val, **variables):
        """ Sets probability of a specific entry in table"""
        assert set(variables) ^ set(self._variables) == set(), "Variables for assignment not Valid for JPT"
        variables = variables.items()
        entrys = [entry for entry in self._entrys if set(entry) | set(variables) == set(entry)]
        if len(entrys) > 1:
            print("ERROR IN SET PROBABILITY JPT")
        else:
            entry = entrys[0]
            self._table[entry] = val


    def __str__(self):
        """ Returns human readable Probability Table"""
        longest_var = max(map(len,self._variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({unc}{given}{cond})".format(unc=", ".join(self._unconditioned),
                                            given=" | " if self._conditioned else "",
                                            cond=", ".join(self._conditioned))
        var_header = str_helper("{vars}".format(vars=" | ".join(self._variables)))
        lst_of_entrys = [" | ".join(map(str_helper, map(lambda x: x[1], k))) + " | " + str(v) for k, v in sorted(self._table.items())]
        table = "\n".join(lst_of_entrys)
        return "{header}\n{rule}\n{var_header}\n{table}".format(table=table, header=header, var_header = var_header, rule="-" * len(header))

    def load_factor(self, string):
        pass

    def loadable_string(self):
        pass

class JPT(Factor):

    def __init__(self, variables, variable_domains):
        """Initializes a Joint Probability Table"""
        super().__init__(variables, set(), variable_domains)

    def valid_table(self):
        """Checks if Probability Rules are followed"""
        assert sum(self._table[entry] for entry in self.get_entrys()) == 1, "JPT does not sum to 1"
        return True if sum(self._table[entry] for entry in self.get_entrys()) == 1 else False

    def get_probability(self, **variables):
        """ Gets probability of certain variables. Includes summing out over vars"""
        # variables = variables.items()
        if len(variables) == 1:
            var = tuple(list(variables.items())[0])
            to_sum = [entry for entry in self._entrys if var in entry]
            return sum(self._table[entry] for entry in to_sum)
        return super().get_probability(**variables)

class CPT(Factor):
    def __init__(self, unconditioned_var, conditioned_vars, variable_domains):
        super().__init__(list(unconditioned_var), conditioned_vars, variable_domains)

    @staticmethod
    def cpts2jpt(cpts):
        """Converts mutliple CPTs to JPT """
        pass
