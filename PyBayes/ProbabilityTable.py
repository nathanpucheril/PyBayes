# Probability Tables Implementation
# ---------------------------------
# @author Nathan Pucheril
# @author Keith Hardaway

from itertools import product
from copy import deepcopy, copy
from warnings import warn
import random
from PyBayes import utils

class Factor(object):
    """ Description:
        Usage:
            -
            -
            -
    """

    def __init__(self, unconditioned_vars, conditioned_vars, variable_domains):
        """ Creates a Factor object that encodes probabilities in a table """
        unconditioned_vars = set(unconditioned_vars)
        conditioned_vars = set(conditioned_vars)

        assert utils.islist_like(unconditioned_vars), "unconditioned_vars must be a list like structure"
        assert utils.islist_like(conditioned_vars), "conditioned_vars must be a list like structure"
        assert isinstance(variable_domains, dict), "variable_domains must be a dict"
        assert all([isinstance(item, str) for item in unconditioned_vars])
        assert unconditioned_vars.isdisjoint(conditioned_vars), "Unconditioned vars and Conditioned Vars must not have the same variable."

        self._domains = variable_domains
        self._variables = set(conditioned_vars) | set(unconditioned_vars)
        self._unconditioned = unconditioned_vars
        self._conditioned = conditioned_vars
        entree_temp = [[(var, domain) for domain in self._domains[var]] for var in self._variables]
        self._entries = list(sorted(product(*entree_temp)))
        self._table = {}
        for entry in self._entries:
            self._table[entry] = 0
        warn("Probabilities not set. Default = 0")

    def get_domains(self):
        return deepcopy(self._domains)

    def get_entrees(self):
        """ Retrieves all possible entries to the table """
        return deepcopy(self._entries)

    def get_probability(self, **variables):
        """ Gets probability of a specific entry in table """
        variables = variables.items()
        if hasattr(variables, "__iter__"):
            to_sum = [entry for entry in self._entries if set(entry) == set(variables)]
            if len(to_sum) != 1:
                raise UserWarning("Error in retrieving probability. Invalid method call.")
            return self._table[to_sum[0]]
        raise UserWarning("Error in retrieving probability. Invalid method call.")
        return 0

    def set_probability(self, val, **variables):
        """ Sets probability of a specific entry in table """
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
        length = len(max(self._variables, key = len))
        def str_beautify(s): return str(s).rjust(length + 2, " ").ljust(length + 3, " ")
        probability = "P({unc}{given}{cond})".format(unc=", ".join(self._unconditioned),
                                                     given=" | " if self._conditioned else "",
                                                     cond=", ".join(self._conditioned))
        var_header = str_beautify(" {vars}".format(vars=" | ".join(map(str_beautify,self._variables))))
        lst_of_entrees = [" | ".join(map(str_beautify, map(lambda x: x[1], k))) + " | " + str(v) for k, v in sorted(self._table.items())]
        table = " \n ".join(lst_of_entrees)
        border_size = (len(var_header) + len(probability) + 5)
        return "{border}\n{var_header} | {probability} \n{rule}\n {table} \n{border}\n\n".format(table=table,
                                                                    probability=probability,
                                                                    var_header = var_header,
                                                                    rule="-" * border_size,
                                                                    border = "*" * border_size
                                                                    )

    def __eq__(self, object2):
        return type(self) == type(object2) and \
               self._unconditioned == object2._unconditioned and \
               self._conditioned == object2._conditioned and \
               self._entries == object2._entries and \
               all([self._table[entry] == object2._table[entry] for entry in self._entries])

    def load_factor(self, string):
        pass

    def loadable_string(self):
        pass

class JPT(Factor):

    def __init__(self, variables, variable_domains):
        """Initializes a Joint Probability Table """
        super().__init__(variables, set(), variable_domains)
        if not self.valid_table():
            warn("JPT is not valid!")

    def valid_table(self):
        """Checks if Probability Rules are followed """
        return True if sum(self._table[entry] for entry in self.get_entrees()) == 1 else False

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
        super().__init__(set([unconditioned_var]), set(conditioned_vars), variable_domains)

    @staticmethod
    def cpts2jpt(cpts):
        """Converts mutliple CPTs to JPT """
        all_domains = {}
        for cpt in cpts:
            all_domains.update(cpt.get_domains())
        jpt = JPT(all_domains.keys(), all_domains)
        jpt_entrees = jpt.get_entrees()
        for entry in jpt_entrees:
            prob = 1
            for cpt in cpts:
                for cpt_entree in cpt.get_entrees():
                    if set(cpt_entree) | set(entry) == set(entry): # Union of CPT and JPT does not yield new Vars
                        prob *= cpt.get_probability(**dict(cpt_entree)) #shouldnt have to put entry in dict
            jpt.set_probability(prob, **dict(entry))#shouldnt have to put entry in dict
        return jpt

    @staticmethod
    def random_cpt(unconditioned_var, conditioned_vars, variable_domains):
        r = CPT(unconditioned_var, conditioned_vars, variable_domains)



def variable_elimination(elimination_var, factors):
    pass
