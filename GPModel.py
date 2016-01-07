import numpy as np
import Utils
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, RationalQuadratic, WhiteKernel

"""
    Wrapper for GaussianProcessRegressor
    
    This class allows custom X, y formatting to be paired with a gaussian process,
    so that we can use a gaussian process model (GPModel) instance on externally
    formatted data (e.g., a dataframe), and the data will be automagically converted
    into and out of GaussianProcessRegressor format when we call fit() or predict()
    (Data is converted using the formatter object we supply in the constructor)
"""

class GPModel(object):

    def __init__(self, formatter):
        self.formatter = formatter

    # Fit model for given params and data
    def fit(self, p, X_y_external):
        # Format training data
        X, y, variance = self.formatter.format_X_y(X_y_external)
        n = len(y)
        # Create gp kernel using params
        kernel = 3.5**2 * RBF(length_scale=float(p["rbf_ls_init"]),
                               length_scale_bounds=(float(p["rbf_ls_lb"]), float(p["rbf_ls_ub"])))
        if("rq_a_init" in p):
            kernel = kernel + 1.05**2 * RationalQuadratic(
                    alpha=float(p["rq_a_init"]),
                    alpha_bounds=(float(p["rq_a_lb"]), float(p["rq_a_ub"])),
                    length_scale=float(p["rq_ls_init"]),
                    length_scale_bounds=(float(p["rq_ls_lb"]), float(p["rq_ls_ub"])))
        if("wk_var_mult_lb" in p):
            kernel = kernel + WhiteKernel(noise_level=0.5 * variance,
                                          noise_level_bounds=(float(p["wk_var_mult_lb"]) * variance,
                                                              float(p["wk_var_mult_ub"]) * variance))
        # Fit gaussian process
        before = Utils.timestamp()
        self.gpr = GaussianProcessRegressor(kernel=kernel, alpha=variance * float(p["alpha_var_multiplier"]),
            n_restarts_optimizer=int(p["n_restarts_optimiser"]), normalize_y=True)
        self.gpr.fit(X, y)
        # Log the time it took
        time_taken = Utils.timestamp() - before
        info_line = "GP ~ n = " + str(n) + ", mins: " + str(time_taken / 60.0) + ", K = " + str(self.gpr.kernel_) + "\n"
        with open("results.txt", "a") as resfile:
            resfile.write(info_line)
        return str(self.gpr.kernel_)

    # Format external input X values, predicts y values, returns formatted output
    def predict(self, X_external):
        X = self.formatter.format_X(X_external)
        y, sigma = self.gpr.predict(X, return_std=True)
        return self.formatter.format_y_sigma(y, sigma)


