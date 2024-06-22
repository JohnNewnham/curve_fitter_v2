import numpy as np

"""
This specific file is intended for the user to change.
This will allow the user to be able to set any function they want for the fit without overriding any of the presets.

Simply change num_of_const, then change the A, B, C, D coefficients to be equal in number to num_of_const, then 
change the equation at the bottom, using the A, B, C etc. coefficients to give an equation in the desired form.
"""

# Number of constants in the function you're fitting to.
num_of_const = 4

# The function which the line will fit to.
def fit_function(x, *args):
    
    # Allows either a single list containing all of the coefficients to be passed in or the coefficients to be passed in as
    # individual arguments by unpacking the list from the tuple if a list is passed in.
    if type(args[0]) == list:
        args = args[0]
    
    # Define coefficients here from args to be used in the equation.
    A = args[0]
    B = args[1]
    C = args[2]
    D = args[3]
    
    # The following equation contains the form of the line you wish to fit to your data.
    # It is assumed that you pass in the data corresponding to the x axis as defined in the previous cell to return the y axis.
    """Change this equation and the coefficient definitions above to change the form of the equation."""
    y = A*np.exp(-B*(x-C)**2) + D
    
    return y

if __name__ == "__main__":
    pass