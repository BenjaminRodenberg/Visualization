__author__ = 'benjamin'

import numpy as np
import convolution_functions as cf

# general settings
# visu
x_min_view=-2
x_max_view=2
y_min_view=-2
y_max_view=2

# sampling
x_min=-10
x_max=10
y_min=-10
y_max=10
resolution=2000.0

#function input
function1_input_msg = "Choose 'my own function' for entering a function here!"
function2_input_msg = "Choose 'my own function' for entering a function here!"
function1_input_init = "sin(x*pi) * Heaviside( x+1 ) * Heaviside(1-x)"
function2_input_init = "sin(x*pi) * Heaviside( x+1 ) * Heaviside(1-x)"

#fourierseries
timeinterval_start = -np.pi
timeinterval_end = +np.pi
timeinterval_length = timeinterval_end-timeinterval_start

#different functions available
function_library = [cf.ramp, cf.window, cf.saw, cf.parser]
function_names = ["Ramp", "Window", "Saw", "my own function"]
default_function_id = 3

# settings for controls
# control function type
function_init = 0

# control degree
x_value_min=x_min
x_value_max=x_max
x_value_step=.1
x_value_init=0


