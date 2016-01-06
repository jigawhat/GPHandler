import sys
from GPRequester import submit_gp_request
from PredictionPlotter import predict_and_plot_all

gp_req = int(float(sys.argv[1])) if(len(sys.argv) > 1) else 0
aid = int(float(sys.argv[2])) if(len(sys.argv) > 2) else 10
fn_suffix = sys.argv[3] if(len(sys.argv) > 3) else ""

request = {
    'dataset': 'landreg',
    'id': aid,
    'params': {
        'logadj': 1.2,
        'filename_suffix': fn_suffix
    }
}
if gp_req:
    submit_gp_request(request)
predict_and_plot_all("landreg", aid, fn_suffix)
