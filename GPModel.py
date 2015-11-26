import numpy as np
import Utils
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, RationalQuadratic, WhiteKernel

class GPModel(object):

    def __init__(self, X, y, params, data_formatter):
        self.formatter = data_formatter
        variance = np.var(y)
        n = len(y)
        print("Creating GP Model, n = " + str(n))

        # TODO add slicing if dataset too large
        # TODO add multiple kernel combinations as model parameters

        # Create gaussian process and fit to data
        kernel = 5.82**2 * RBF(length_scale=32.0, length_scale_bounds=tuple(params["RBF_length_scale_bounds"])) + \
                0.319**2 * RationalQuadratic(alpha=0.1, alpha_bounds=tuple(params["rational_quadratic_alpha_bounds"]),
                    length_scale=0.1, length_scale_bounds=tuple(params["rational_quadratic_length_scale_bounds"]))
        before = Utils.timestamp()
        self.gpr = GaussianProcessRegressor(kernel=kernel, alpha=variance * params["variance_multiplier"],
            n_restarts_optimizer=int(params["n_restarts_optimizer"]), normalize_y=(int(params["normalize_y"]) == 1))
        self.gpr.fit(X, y)

        # Log the time it took
        time_taken = Utils.timestamp() - before
        info_line = "GP ~ n = " + str(n) + ", mins: " + str(time_taken / 60.0) + ", K = " + str(self.gpr.kernel_) + "\n"
        with open("results.txt", "a") as resfile:
            resfile.write(info_line)
        print("Created.")

    def predict(self, X):
        return self.gpr.predict(X, return_std=True)

    def predict_and_format(self, X_external_format):
        X = self.formatter.format_input_X(X_external_format)
        y, sigma = predict(X)
        return format_output_y_sigma(y, sigma)


