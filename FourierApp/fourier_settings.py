__author__ = 'benjamin'

import numpy as np
import fourier_functions as ff

# general settings
# plotting
x_min=0
x_max=2*np.pi
y_min=-2.5
y_max=2.5
resolution=200

#fourierseries
timeinterval_start = x_min
timeinterval_end = x_max
timeinterval_length = timeinterval_end-timeinterval_start

#different functions available
function_library = [ff.hat,ff.step,ff.saw]
function_names = ["Hat", "Step", "Saw"]

# settings for controls
# control function type
function_init = 0

# control degree
degree_min=0
degree_max=20
degree_step=1
degree_init=5


