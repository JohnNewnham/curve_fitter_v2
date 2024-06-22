from repository import Repository
from scipy.optimize import curve_fit
import numpy as np

def propagate_errors(repo):
    """
    This cell calculates errors on the coefficients using Monte-Carlo error propagation.
    It repeatedly varies the position of the points within their errors, performing a fit for coefficients each time, then takes
    the standard deviation of the resulting set of fitted coefficients.
    """

    # Only bothers to calculate the errors if there are any.
    if repo.settings["has_x_errors"] or repo.settings["has_y_errors"]:
        
        # Creates a list containing empty sublists. Each sublist will contain many values for the same coefficient.
        varying_const_list = [[] for _ in range(repo.settings["num_of_const"])]
        
        # Repeats as many times as specified.
        for _ in range(repo.settings["monte_carlo_repeats"]):
            
            # Generates x and y data to fit a curve to by varying the position of each point by random values in x and y
            # given by a normal distribution with standard deviation given by the errors.
            if repo.settings["has_x_errors"]:
                test_x_data = repo.x_data + np.random.normal(scale=repo.x_errs)
            else:
                test_x_data = repo.x_data

            if repo.settings["has_y_errors"]:
                test_y_data = repo.y_data + np.random.normal(scale=repo.y_errs)
            else:
                test_y_data = repo.y_data
            
            # Fits a curve to these randomly varied points.
            parameters, covariance = curve_fit(repo.fit_func, test_x_data, test_y_data, p0=repo.coeffs_fitted)
            
            # Adds the values of the coefficients to the varying_const_list sublists.
            for i in range(repo.settings["num_of_const"]):
                varying_const_list[i].append(parameters[i])
        
        # Creates a list to store the values of the errors on each coefficient.
        const_err = []
        # For each coefficient it calculates the error, adds it to the list, then prints the value of the coefficient along with
        # its error.
        for i in range(repo.settings["num_of_const"]):
            const_err.append(np.std(varying_const_list[i]))
            print(f"Coefficient {i+1}: {repo.coeffs_fitted[i]} ± {const_err[i]}")
        
        # Transfer the errors to the repository and return it.
        repo.coeffs_error = const_err
    return repo