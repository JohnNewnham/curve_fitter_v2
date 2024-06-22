from repository import Repository
from monte_carlo import propagate_errors
from fit_funcs import *
from funcs import *
import numpy as np
import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

repo = Repository()
repo.loadData()
generate_x_fitted(repo)
        
class Window():

    def __init__(self):
        # Create a window and set its icon and title.
        self.root = tk.Tk()
        self.root.title("Line fitter")
        self.root.iconphoto(False, tk.PhotoImage(file="fitter_images/icon.png"))
        self.root.withdraw()

        # Gain input from user on number of constants used before opening the full window. Disabled now that it is built in to the fit functions.
        global repo
        # obtain_num_of_const(repo)
        self.root.deiconify()

        # Create and pack the frames to put the input and output in respectively.
        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)
        self.frame1.pack(fill=tk.X, expand=True, side=tk.LEFT, pady=(20, 40), padx=50)
        self.frame2.pack(fill=tk.X, expand=True, side=tk.RIGHT, pady=(20, 40), padx=50)

        # Create lists to store the labels, entries and variables in the frames.
        self.input_labels = []
        self.input_entries = []
        self.input_double_vars = []
        self.output_labels = []
        self.output_string_vars = []

        # Create the labels, entries and variables and pack them into the frames.
        self.update_window()

        # Create the menubar.
        self.menubar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.func_menu = tk.Menu(self.menubar, tearoff=0)
        # Create the options.
        self.file_menu.add_command(label="Save settings", command=repo.saveSettings)
        self.file_menu.add_command(label="Load default settings", command=lambda: self.change_settings(True))
        self.file_menu.add_command(label="Load saved settings", command=lambda: self.change_settings(False))
        self.settings_menu.add_command(label="Change number of constants", command=self.update_num_of_const)
        self.settings_menu.add_command(label="Rename X axis", command=lambda: self.rename_axis("X"))
        self.settings_menu.add_command(label="Rename Y axis", command=lambda: self.rename_axis("Y"))
        self.has_x_err_var = tk.BooleanVar()
        self.has_x_err_var.set(repo.settings["has_x_errors"])
        self.settings_menu.add_checkbutton(label="Include X axis errors", 
                                           onvalue=True, 
                                           offvalue=False, 
                                           variable=self.has_x_err_var, 
                                           command=lambda: self.toggle_errs("X"))
        self.has_y_err_var = tk.BooleanVar()
        self.has_y_err_var.set(repo.settings["has_y_errors"])
        self.settings_menu.add_checkbutton(label="Include Y axis errors", 
                                           onvalue=True, 
                                           offvalue=False, 
                                           variable=self.has_y_err_var, 
                                           command=lambda: self.toggle_errs("Y"))
        self.settings_menu.add_command(label="Select file", command=lambda: select_file(repo))
        self.settings_menu.add_command(label="Change Monte Carlo repeats", command=lambda: change_repeats(repo))
        self.settings_menu.add_command(label="Print settings", command=lambda: self.print_repo_settings())
        self.func_menu.add_radiobutton(label="Gaussian", command=lambda: self.change_func(gaussian))
        self.func_menu.add_radiobutton(label="Exponential", command=lambda: self.change_func(exponential))
        self.func_menu.add_radiobutton(label="Logarithmic", command=lambda: self.change_func(log))
        self.func_menu.add_radiobutton(label="Sinusoid", command=lambda: self.change_func(sine))
        self.func_menu.add_radiobutton(label="Linear", command=lambda: self.change_func(linear))
        self.func_menu.add_radiobutton(label="Quadratic", command=lambda: self.change_func(quadratic))
        self.func_menu.add_radiobutton(label="Cauchy distribution", command=lambda: self.change_func(cauchy))
        self.func_menu.add_radiobutton(label="Custom", command=lambda: self.change_func(custom))
        # Add the menubar to the window.
        self.menubar.add_cascade(menu=self.file_menu, label="File")
        self.menubar.add_cascade(menu=self.settings_menu, label="Settings")
        self.menubar.add_cascade(menu=self.func_menu, label="Select function")
        self.root.config(menu=self.menubar)

        # Set a check to be run when the user tries to close the window.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Enter the mainloop.
        self.root.mainloop()

    def update_window(self):
        # Empty the frames.
        for widget in self.frame1.winfo_children(): widget.destroy()
        for widget in self.frame2.winfo_children(): widget.destroy()

        # Empty the lists storing the labels, entries and variables that were in the frames.
        self.input_labels = []
        self.input_entries = []
        self.input_double_vars = []
        self.output_labels = []
        self.output_string_vars = []

        # Populate frame1.
        for i in range(repo.settings["num_of_const"]):
            # Create and pack the label above each input box.
            self.input_labels.append(tk.Label(self.frame1,
                                              text="Input a guess for " + [*"ABCDEFGHIJKLMNOPQRSTUVWXYZ"][i] + ":",
                                              fg="black",
                                              font=repo.label_font))
            self.input_labels[-1].pack(pady=10)

            # Create and pack the input boxes.
            self.input_double_vars.append(tk.DoubleVar())
            self.input_double_vars[-1].set(value=repo.coeffs_guessed[i])
            self.input_double_vars[-1].trace_add("write", self.entry_callback)
            self.input_entries.append(tk.Entry(self.frame1,
                                               textvariable=self.input_double_vars[i],
                                               font=repo.label_font))
            self.input_entries[-1].pack(pady=10)

        # Make a button to go under the input boxes to display the graph.
        self.update_button = tk.Button(self.frame1,
                                       text="Show Graph",
                                       bg="red",
                                       fg="white",
                                       command=lambda: self.update_estimate_graph(),
                                       font=repo.label_font,
                                       width=15)
        self.update_button.pack(pady=10)

        # Make a button to perform the fit and display output.
        self.update_button = tk.Button(self.frame1,
                                       text="Fit line",
                                       bg="green",
                                       fg="white",
                                       command=lambda: self.update_fitted_graph(),
                                       font=repo.label_font,
                                       width=15)
        self.update_button.pack(pady=10)

        # Populate frame2.
        for i in range(repo.settings["num_of_const"]):
            # Create and pack the label above each output.
            self.output_labels.append(tk.Label(self.frame2,
                                            text="Fitted value for " + [*"ABCDEFGHIJKLMNOPQRSTUVWXYZ"][i] + ":",
                                            fg="black",
                                            font=repo.label_font))
            self.output_labels[-1].pack(pady=10)

            # Create and pack the label for each output, along with its string variable.
            self.output_string_vars.append(tk.StringVar())
            self.output_string_vars[i].set(value=" \n ")
            self.output_labels.append(tk.Label(self.frame2,
                                            textvariable=self.output_string_vars[i],
                                            bg="white",
                                            width=20,
                                            font=repo.label_font))
            self.output_labels[-1].pack(pady=10)

    def entry_callback(self, var, index, mode):
        if plt.fignum_exists(1): self.update_estimate_graph()

    def update_estimate_graph(self):
        try:
            self.update_coeffs_guessed()
        except:
            return
        display_estimate_plot(repo)
    
    def update_fitted_graph(self):
        try:
            self.update_coeffs_guessed()
        except:
            tk.messagebox.showwarning(title="Error", message="Input values must be numbers.")
            return
        try:
            global repo
            display_fitted_plot(repo)
        except:
            tk.messagebox.showwarning(title="Error", message="Error in fitting line.\nTry more accurate estimates.")
            return
        try:
            repo = propagate_errors(repo)
        except:
             tk.messagebox.showwarning(title="Error", message="Error in propagating errors.\nCheck number of Monte Carlo repeats.")
             return
        self.update_text_output(repo)
    
    def update_coeffs_guessed(self):
            coeffs_guessed = [self.input_double_vars[i].get() for i in range(repo.settings["num_of_const"])]
            repo.coeffs_guessed = coeffs_guessed

    def update_text_output(self, repo):
        for i in range(repo.settings["num_of_const"]):
            output_string = '{:g}'.format(float('{:.{p}g}'.format(repo.coeffs_fitted[i], p=repo.settings["output_sig_figs"])))
            output_string += "\n"+u"\u00B1"
            if repo.settings["has_x_errors"] or repo.settings["has_y_errors"]:
                output_string += '{:g}'.format(float('{:.{p}g}'.format(repo.coeffs_error[i], p=repo.settings["output_sig_figs"])))
            else:
                output_string += '{:g}'.format(float('{:.{p}g}'.format(0, p=repo.settings["output_sig_figs"])))
            self.output_string_vars[i].set(output_string)

    def update_num_of_const(self):
        global repo
        obtain_num_of_const(repo)
        repo.updateCoeffLists()
        self.update_window()

    def change_settings(self, default=True):
        global repo
        repo.loadSettings(default)
        self.update_window()

    def rename_axis(self, axis):
        global repo
        answer = simpledialog.askstring(f"Rename {axis} axis", f"Input the new name for\nthe {axis} axis:")
        if answer is None:
            return
        else:
            repo.settings[axis.lower()+"_axis_name"] = answer
            if plt.fignum_exists(1): self.update_estimate_graph()

    def toggle_errs(self, axis):
        global repo
        if axis.upper() == "X":
            repo.settings["has_x_errors"] = self.has_x_err_var.get()
        elif axis.upper() == "Y":
            repo.settings["has_y_errors"] = self.has_y_err_var.get()
        else:
            raise ValueError("Input to toggle_errs must be X or Y.")
        repo.loadData()
        display_estimate_plot(repo)

    def print_repo_settings(self):
        bar_length = 15
        print(bar_length*"-")
        for key, value in repo.settings.items(): print(f"{key}: {value}")
        print(bar_length*"-")

    def change_func(self, module):
        global repo
        repo.fit_func = module.fit_function
        repo.settings["num_of_const"] = module.num_of_const
        repo.updateCoeffLists()
        self.update_window()
        display_estimate_plot(repo)

    def on_closing(self):
	        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
	        	self.root.destroy()



if __name__ == "__main__":
    Window()