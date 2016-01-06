import numpy as np
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from GPRequester import submit_gp_request
from PredictionPlotter import predict_and_plot_all

aid = 10
fn_suffix = "_logadj_test"

request = {
    'dataset': 'landreg',
    'id': aid,
    'params': {
        'logadj': 1.2,
        'filename_suffix': fn_suffix
    }
}

submit_gp_request(request)
predict_and_plot_all("landreg", aid, fn_suffix)
