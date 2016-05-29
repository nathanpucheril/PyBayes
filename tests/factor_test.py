import pytest

from PyBayes.ProbabilityTable import Factor

class TestFactor:

    def test_factor_input1(self):
        """ Checks if inputs to Factor for Unconditioned Vars is Handled Properly """
        with pytest.raises(AssertionError):
            Factor("",[],{})

    def test_factor_input2_1(self):
        """ Checks if inputs to Factor for Unconditioned Vars is Handled Properly """
        with pytest.raises(AssertionError):
            Factor([],"",{})

    def test_factor_input2_2(self):
        """ Checks if inputs to Factor for Unconditioned Vars is Handled Properly """
        try:
            Factor([],tuple(),{})
        except:
            pytest.fail("Error when there shouldn't have been. >>> Factor([],tuple(),{}) is valid")

    def test_factor_input2_3(self):
        """ Checks if inputs to Factor for Unconditioned Vars is Handled Properly """
        try:
            Factor([],set(),{})
        except:
            pytest.fail("Error when there shouldn't have been. >>> Factor([],set(),{}) is valid")

    def test_factor_input3(self):
        """ Checks if inputs to Factor for Unconditioned Vars is Handled Properly """
        with pytest.raises(AssertionError):
            Factor([],[],[])
