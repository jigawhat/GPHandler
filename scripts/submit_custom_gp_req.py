import numpy as np
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from GPRequester import submit_gp_request

request = {
    'dataset': 'landreg',
    'id': 7,
    'params': {
        'logadj': 1.2,
        'filename_suffix': "_logadj_test"
    }
}
submit_gp_request(request)


