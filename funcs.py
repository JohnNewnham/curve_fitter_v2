from repository import Repository
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox, simpledialog
import tkinter as tk
from os import listdir
from os.path import realpath
import sys

def generate_x_fitted(repo):
    start = repo.x_data.min() - 0.1*(repo.x_data.max()-repo.x_data.min())
    end = repo.x_data.max() + 0.1*(repo.x_data.max()-repo.x_data.min())

    repo.x_fitted = np.arange(start, end, (end-start)/repo.settings["fitted_point_count"])

def display_fitted_plot(repo):
    parameters, covariance = curve_fit(repo.fit_func, 
                                       repo.x_data, 
                                       repo.y_data, 
                                       p0=repo.coeffs_guessed)
    
    repo.coeffs_fitted = [parameters[i] for i in range(repo.settings["num_of_const"])]

    repo.y_fitted = repo.fit_func(repo.x_fitted, repo.coeffs_fitted)

    # Clears plot.
    plt.clf()

    # Plots the fit for comparison to the experimental data.
    plt.plot(repo.x_fitted, 
            repo.y_fitted, 
            "red", 
            label ="Fitted line")

    # Plots the experimental data for comparison to the fit.
    plt.errorbar(repo.x_data, 
                repo.y_data, 
                xerr =repo.x_errs, 
                yerr =repo.y_errs, 
                fmt =".k", 
                ecolor ="b", 
                capsize =2, 
                label ="Experimental results")

    # Plot formatting.
    plt.xlabel(repo.settings["x_axis_name"])
    plt.ylabel(repo.settings["y_axis_name"])
    plt.legend(loc="upper left")
    plt.show()

def display_estimate_plot(repo):
    y_estimate = repo.fit_func(repo.x_fitted, repo.coeffs_guessed)

    # Clears plot.
    plt.clf()

    # Plots the estimate for comparison to the experimental data.
    plt.plot(repo.x_fitted, 
            y_estimate, 
            "red", 
            label ="Estimated line")
    
    # Plots the experimental data for comparison to the fit.
    plt.errorbar(repo.x_data, 
                repo.y_data, 
                xerr =repo.x_errs, 
                yerr =repo.y_errs, 
                fmt =".k", 
                ecolor ="b", 
                capsize =2, 
                label ="Experimental results")
    
    # Plot formatting.
    plt.xlabel(repo.settings["x_axis_name"])
    plt.ylabel(repo.settings["y_axis_name"])
    plt.legend(loc="upper left")
    plt.show()

def obtain_num_of_const(repo):
    # Enter a loop until a valid input is entered.
    while True:
        answer = simpledialog.askinteger("Number of constants", "Input the number of constants in the\nequation you are using for the line fit.")
        # Check for NoneType (cancel).
        if answer is None:
            sys.exit()
        else:
            # Check for a positive integer and one less than 8.
            # 7 is a hard coded maximum due to window size. 
            # Will consider recoding using a scrollable window for a future version supporting up to 26.
            if (answer <= 0) or (answer > 7):
                messagebox.showwarning(title="Error", message="Input values must be positive\nand less than 8.")
            else:
                # Check to see if the number of coefficients works with the fit function.
                try:
                    repo.fit_func(1,[1 for _ in range(answer)])
                except:
                    messagebox.showwarning(title="Error", message="Error in the fit function.\nToo few coefficients\ndefined before equation?")
                else:
                    repo.settings["num_of_const"] = answer
                    break

def change_repeats(repo):
    # Enter a loop until a valid input is entered.
    while True:
        answer = simpledialog.askinteger("Number of repeats", "Input the number of Monte Carlo repeats you\nwould like to use for error propagation.")
        # Check for NoneType (cancel).
        if answer is None:
            break
        else:
            # Check for a positive integer and one less than 8.
            # 7 is a hard coded maximum due to window size. 
            # Will consider recoding using a scrollable window for a future version supporting up to 26.
            if (answer <= 0) or (answer > 1_000_000):
                messagebox.showwarning(title="Error", message="Input values must be positive\nand less than 1,000,000.")
            else:
                repo.settings["monte_carlo_repeats"] = answer
                break

def select_file(repo):
    # Get all csv files from the "data" folder.
    csv_list = [file for file in listdir(realpath(__file__)[:-8]+"data\\") if file[-4:] == ".csv"]

    # Make a window for the user to select a file from.
    sub_window = tk.Toplevel()
    sub_window.title("Change file")
    sub_window.iconphoto(False, tk.PhotoImage(file="fitter_images/icon.png"))

    # When they select one it extracts the result and closes.
    filename = None
    csv_chosen = tk.StringVar(sub_window, csv_list[0])
    def return_result():
        filename = csv_chosen.get()
        sub_window.destroy()

        # Make a second window for the user to input the column numbers in.
        sub_window_2 = tk.Toplevel()
        sub_window_2.title("Enter columns")
        sub_window_2.iconphoto(False, tk.PhotoImage(file="fitter_images/icon.png"))

        x_data_label = tk.Label(sub_window_2, text="Input the column number for the X axis data:", fg="black", font=repo.label_font)
        x_errs_label = tk.Label(sub_window_2, text="Input the column number for the X axis errors:", fg="black", font=repo.label_font)
        y_data_label = tk.Label(sub_window_2, text="Input the column number for the Y axis data:", fg="black", font=repo.label_font)
        y_errs_label = tk.Label(sub_window_2, text="Input the column number for the Y axis errors:", fg="black", font=repo.label_font)

        x_data_var = tk.StringVar()
        x_errs_var = tk.StringVar()
        y_data_var = tk.StringVar()
        y_errs_var = tk.StringVar()

        x_data_entry = tk.Entry(sub_window_2, font=repo.label_font, textvariable=x_data_var)
        x_errs_entry = tk.Entry(sub_window_2, font=repo.label_font, textvariable=x_errs_var)
        y_data_entry = tk.Entry(sub_window_2, font=repo.label_font, textvariable=y_data_var)
        y_errs_entry = tk.Entry(sub_window_2, font=repo.label_font, textvariable=y_errs_var)

        # Return all the values when a "done" button is pressed.
        def return_result_2():
            try:
                outputs = {}
                outputs["x_data_column"] = int(x_data_var.get())
                outputs["x_error_column"] = int(x_errs_var.get())
                outputs["y_data_column"] = int(y_data_var.get())
                outputs["y_error_column"] = int(y_errs_var.get())
            except:
                messagebox.showwarning(title="Error", message="Please input integer values.")
            else:
                valid = True
                for output in outputs.values():
                    if output < 0:
                        messagebox.showwarning(title="Error", message="Please input positive values.")
                        valid = False
                if valid:
                    repo.settings["filename"] = filename
                    repo.settings["x_data_column"] = outputs["x_data_column"]
                    repo.settings["x_error_column"] = outputs["x_error_column"]
                    repo.settings["y_data_column"] = outputs["y_data_column"]
                    repo.settings["y_error_column"] = outputs["y_error_column"]
                    repo.loadData()
                    generate_x_fitted(repo)
                    sub_window_2.destroy()

        done_button = tk.Button(sub_window_2, bg="green", font=repo.label_font, text="Done", command=return_result_2)

        x_data_label.pack()
        x_data_entry.pack()
        x_errs_label.pack()
        x_errs_entry.pack()
        y_data_label.pack()
        y_data_entry.pack()
        y_errs_label.pack()
        y_errs_entry.pack()
        done_button.pack()

        sub_window_2.mainloop()

    radio_list = [tk.Radiobutton(sub_window, text=file, variable=csv_chosen, value=file, command=return_result) for file in csv_list]
    for button in radio_list: button.pack(anchor="w")

    sub_window.mainloop()