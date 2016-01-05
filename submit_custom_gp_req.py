import numpy as np
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from GPRequester import submit_gp_request

loader = DataLoader()

def submit_gp_req(dataset, aid, new_params, fn_suffix):
    params = loader.load_params_for_aid(dataset, aid)

    for key in new_params:
        params[key] = new_params[key]

    params["filename_suffix"] = fn_suffix
    request = {
        'dataset': 'landreg',
        'id': aid,
        'params': params
    }
    submit_gp_request(request)


p = {
    'rbf_ls_init': 70.0,
    'rbf_ls_lb': 0.1,
    'rbf_ls_ub': 1000.0,
    'rq_a_init': 0.01,
    'rq_a_lb': 0.01,
    'rq_a_ub': 10.0,
    'rq_ls_init': 0.1,
    'rq_ls_lb': 0.1,
    'rq_ls_ub': 100.0,
}

submit_gp_req("landreg", 2523, p, "_rq_adj_1")
