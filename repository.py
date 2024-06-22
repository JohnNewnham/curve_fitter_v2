import numpy as np
import json
from fit_funcs import *
from fit_funcs import *

if __name__ == "__main__":
    pass

"""
This class will store all of the data so that it can be passed from one python file to another easily.

If all variables are stored within this class then each function can simply take the repository as input and return the repository.
"""

class Repository():

    def __init__(self):

        self.x_data = np.array([])
        self.y_data = np.array([])
        self.x_errs = np.array([])
        self.y_errs = np.array([])
        self.x_fitted = np.array([])
        self.y_fitted = np.array([])
        self.coeffs_guessed = []
        self.coeffs_fitted = []
        self.coeffs_error = []
        self.label_font = ('Arial', 14)
        self.fit_func = gaussian.fit_function

        self.loadSettings(False)
        self.settings["num_of_const"] = gaussian.num_of_const
    
    def loadData(self):
        # Import the values as floats. If there are headings they will be caught by the try except.
        try:
            imported_csv = np.loadtxt("data/"+self.settings["filename"], delimiter=",", dtype=float)
        except:
            imported_csv = np.loadtxt("data/"+self.settings["filename"], delimiter=",", skiprows=1, dtype=float)
        
        self.x_data = imported_csv[:,self.settings["x_data_column"]]
        self.y_data = imported_csv[:,self.settings["y_data_column"]]
        self.x_errs = imported_csv[:,self.settings["x_error_column"]] if self.settings["has_x_errors"] else None
        self.y_errs = imported_csv[:,self.settings["y_error_column"]] if self.settings["has_y_errors"] else None

    def saveSettings(self):
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)

    def loadSettings(self, default=True):
        if default:
            file = open('default_settings.json')
        else:
            file = open('settings.json')
        self.settings = json.load(file)
        self.updateCoeffLists()
        file.close()
    
    def updateCoeffLists(self):
        # Resize the lists according to the number of constants without losing current values.
        if self.settings["num_of_const"] > len(self.coeffs_guessed):
            self.coeffs_guessed += [1 for _ in range(self.settings["num_of_const"]-len(self.coeffs_guessed))]
            self.coeffs_fitted += [1 for _ in range(self.settings["num_of_const"]-len(self.coeffs_guessed))]
            self.coeffs_error += [1 for _ in range(self.settings["num_of_const"]-len(self.coeffs_guessed))]
        else:
            self.coeffs_guessed = self.coeffs_guessed[:self.settings["num_of_const"]]
            self.coeffs_fitted = self.coeffs_guessed[:self.settings["num_of_const"]]
            self.coeffs_error = self.coeffs_guessed[:self.settings["num_of_const"]]