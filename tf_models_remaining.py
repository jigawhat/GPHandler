'''
    Prints the number of trend optimiser models remaining for a given area id
'''

import os
import sys
import json

aid = sys.argv[1] if(len(sys.argv) > 1) else 0

model_save_path = "modelsaves/"
config_file = open("trend_optimiser_config.json")
conf = json.load(config_file)

def model_not_present(path):
    return not os.path.isfile(path + "/gp_model.pkl")

dataset = conf["dataset"]
fold_years = conf["fold_years"]
folds = conf["folds"]
log_scales = conf["log_scales"]

models_remaining = 0

for fold in folds:
    for i in range(len(log_scales)):
        fn_suffix = "_" + str(fold) + "_" + ("normal" if i == 0 else ("logadj_sc" + str(i)))
        request = {
            "dataset": dataset,
            "id": str(aid),
            "params": {
                "filename_suffix": fn_suffix,
                "end_date": fold,
                "logadj": 0.0 if i == 0 else 1.2,
                "log_scaling": log_scales[i],
                "save_json": 1.0
            }
        }
        path = model_save_path + dataset + "/" + str(aid) + fn_suffix
        if model_not_present(path):
            models_remaining += 1

sys.stdout.write(str(models_remaining))
sys.stdout.flush()


