# Line Fitter v2.0

A programme used to fit different mathematical functions to data.

## Description

A programme that displays a graph containing input data points and a mathematical line. \
You can adjust the function of the line from the function menu at the top. \
You can adjust the input 'guess' parameters using the input boxes on screen, the graph will update in real time when displayed. \
You can change the data being used from the settings menu. It shows all .csv files in ./data/ \
Once you have 'guess' parameters which make the mathematical line roughly line up with the data you can select "fit line" and coefficients with associated errors will be generated. 

## Required packages
- NumPy
- SciPy
- Matplotlib

## To-do

- [X] Create a programme that can fit a line to data.
- [X] Add a save/load function for the settings.
- [X] Add a menu to be able to change the key settings.
- [X] Add additional presets for the line type (e.g. linear, quadratic etc.).
- [X] Add the ability to change the data used from within the user interface.
- [ ] Clean up user interface layout (especially for loading data).
- [ ] Create clearer instructions on use.
- [ ] Fix slow start up time with code (taking a long time for the window to appear after code is run).