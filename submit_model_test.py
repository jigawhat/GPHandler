import sys
from GPRequester import submit_gp_request
from PredictionPlotter import predict_and_plot_all

gp_req = int(float(sys.argv[1])) if(len(sys.argv) > 1) else 0
plot_req = int(float(sys.argv[2])) if(len(sys.argv) > 2) else 0
aid = int(float(sys.argv[3])) if(len(sys.argv) > 3) else 10
fn_suffix = sys.argv[4] if(len(sys.argv) > 4) else ""

request = {
    'dataset': 'landreg',
    'id': aid,
    'params': {
        # 'wk_var_mult_lb': 0.23,
        # 'wk_var_mult_ub': 0.77,
        'logadj': 1.2,
        'rq_a_ub': 10.0,
        'rq_a_lb': 0.001,
        'rq_ls_ub': 10.0,
        'rq_ls_lb': 0.1,
        'filename_suffix': fn_suffix
    }
}

print request["params"]

if gp_req:
    submit_gp_request(request)
if plot_req:
    predict_and_plot_all("landreg", aid, fn_suffix)
