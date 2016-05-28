from PyBayes.BayesNet import BayesNet
from PyBayes.ProbabilityTable import *

var1 = ["hi", "bye"]
dom1 = {"hi": ["friend", "parent"], "bye": ["friend", "parent"]}
var2 = ["mom", "dad"]
dom2 = {"mom": ["scold", "praise"], "dad": ["scold", "praise"]}

cpt1 = CPT("hi", ["bye"], dom1)
entries = cpt1.get_entrees()
# print(entries)
for entry in entries:
    # print(dict(entry))
    cpt1.set_probability(.2, **dict(entry))


cpt2 = CPT("mom", ["dad"], dom2)
entries = cpt2.get_entrees()
# print(entries)
count = .01
for entry in entries:
    # print(dict(entry))
    cpt2.set_probability(.1 + count, **dict(entry))
    count += .01

print(cpt1)
print(cpt2)

jpt = CPT.cpts2jpt([cpt1, cpt2])
print(jpt)
