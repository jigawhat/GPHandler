import os
import sys
import random
import subprocess
from TrendOptimiser import optimise_trend

first = int(float(sys.argv[1])) if(len(sys.argv) > 1) else 0
last = int(float(sys.argv[2])) if(len(sys.argv) > 2) else first

def model_not_present(path):
    return not os.path.isfile(path + "/gp_model.pkl")

aids = []

for aid in range(first, last + 1):
    if model_not_present("modelsaves/landreg/" + str(aid)):
        aids.append(aid)

print
print "Optimising " + str(len(aids)) + " areas"
# aids = [round(random.random() * 5425) for x in range(15)]

# [2002, 2011, 2013, 2015, 2017, 2506]

lsis = []

for aid in aids:
    lsis.append(optimise_trend(aid))

with open("cv_results.txt", "a") as resfile:
    resfile.write(str(lsis) + "\n")


