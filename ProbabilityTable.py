# Probability Tables Implementation
# ________________________
# @author Nathan Pucheril
# @author Keith Hardaway
from itertools import product, combinations
from copy import deepcopy, copy
from warnings import warn

class Factor(object):
    def __init__(self, unconditioned_vars, conditioned_vars, variable_domains):
        self._domains = variable_domains
        self._variables = set(conditioned_vars) | set(unconditioned_vars)
        self._unconditioned = unconditioned_vars
        self._conditioned = conditioned_vars
        entree_temp = [[(var, domain) for domain in self._domains[var]] for var in self._variables]
        self._entrees = list(sorted([element for element in product(*entree_temp)]))
        self._table = {}
        for entree in self._entrees:
            self._table[entree] = 0
        warn("Probabilities not set. Default = 0")

    def getEntrees(self):
        return self._entrees

    def get_probability(self, **variables):
        variables = variables.items()
        if hasattr(variables, "__iter__"):
            to_sum = [entree for entree in self._entrees if set(entree) == set(variables)]
            if len(to_sum) != 1:
                raise UserWarning("Error in retrieving probability. Invalid method call.")
            return self._table[to_sum[0]]
        raise UserWarning("Error in retrieving probability. Invalid method call.")
        return 0

    def set_probability(self, val, **variables):
        assert set(variables) ^ set(self._variables) == set(), "Variables for assignment not Valid for JPT"
        variables = variables.items()
        entrees = [entree for entree in self._entrees if set(entree) | set(variables) == set(entree)]
        if len(entrees) > 1:
            print("ERROR IN SET PROBABILITY JPT")
        else:
            entree = entrees[0]
            self._table[entree] = val


    def __str__(self):
        longest_var = max(map(len,self._variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({unc}{given}{cond})".format(unc=", ".join(self._unconditioned),
                                            given=" | " if self._conditioned else "",
                                            cond=", ".join(self._conditioned))
        lst_of_entrees = [" | ".join(map(str_helper, k)) + " | " + str(v) for k, v in sorted(self._cpt.items())]
        table = "\n".join(lst_of_entrees)
        cpt_str = "{header}\n{rule}\n{table}".format(table=table, header=header, rule="-" * len(header))
        return cpt_str


class JPT(Factor):

    def __init__(self, variables, variable_domains):
        super().__init__(variables, set(), variable_domains)

    def get_probability(self, **variables):
        # variables = variables.items()
        if len(variables) == 1:
            var = tuple(list(variables.items())[0])
            to_sum = [entree for entree in self._entrees if var in entree]
            return sum(self._table[entree] for entree in to_sum)
        return Factor.get_probability(self, **variables)



    def __str__(self):
        longest_var = max(map(len,self._variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        # print("\n".join(map(str,self._table.items())))
        header = "P({vars})".format(vars=", ".join(self._variables))
        var_header = "{vars}".format(vars=" | ".join(self._variables))
        k,v = sorted(self._table.items())[0]
        print(k, "first")
        print(list())
        lst_of_entrees = [" | ".join(map(str_helper, map(lambda x: x[1], k))) + " | " + str(v) for k, v in sorted(self._table.items())]
        table = "\n".join(lst_of_entrees)
        return "{header}\n{rule}\n{var_header}\n{table}".format(table=table,
                                                                header=header,
                                                                var_header = var_header,
                                                                rule="-" * len(header))


class CPT(Factor):
    def __init__(self, unconditioned_var, conditioned_vars, variable_domains):
        super().__init__(unconditioned_var, conditioned_vars, variable_domains)

    def __str__(self):
        longest_var = max(map(len,self._variables))
        def str_helper(s): return str(s).rjust(longest_var, " ").ljust(longest_var, " ")
        header = "P({unc} | {cond})".format(unc=self._unconditioned,
                                            cond=", ".join(self._conditioned))
        lst_of_entrees = [" | ".join(map(str_helper, k)) + " | " + str(v) for k, v in sorted(self._cpt.items())]
        table = "\n".join(lst_of_entrees)
        cpt_str = "{header}\n{rule}\n{table}".format(table=table, header=header, rule="-" * len(header))
        return cpt_str
