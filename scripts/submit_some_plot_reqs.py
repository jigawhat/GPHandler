from PredictionPlotter import predict_and_plot_all

for i in range(2525, 2550):
# for i in [2506, 2513, 2516, 2519, 2520]:
    predict_and_plot_all("landreg", i, "")
    predict_and_plot_all("landreg", i, "_logadj")
