import numpy as np
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from GPRequester import submit_gp_request

loader = DataLoader()

def submit_test_gp_model(dataset, aid, fold_year):
    params = loader.load_params_for_aid(dataset, aid)
    params["end_date"] = fold_year
    params["filename_suffix"] = "_fold_" + str(fold_year)
    request = {
        'dataset': 'landreg',
        'id': aid,
        'params': params
    }
    submit_gp_request(request)


submit_test_gp_model("landreg", 3247, 2013.0)
