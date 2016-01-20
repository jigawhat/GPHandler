import sys
from PredictionPlotter import predict_and_plot_all

first = int(float(sys.argv[1])) if(len(sys.argv) > 1) else 0
last = int(float(sys.argv[2])) if(len(sys.argv) > 2) else 5425
fn_suffix = sys.argv[3] if(len(sys.argv) > 3) else ""

for i in range(first, last + 1):
    predict_and_plot_all("landreg", i, fn_suffix)
    
