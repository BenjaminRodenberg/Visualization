__author__ = 'benjamin'

#some constants used in the ode_app
#general
max_time = 5        # max time for ode scheme
min_time = 0 # DONT CHANGE THIS!
max_y = 3.5
min_y = -1.5

#constants for logistic equation
logistic_k = 5      #
logistic_g = .5     #

#constants for dahlquist test equation
dahlquist_lambda = -5   # parameter y'=lambda*y

#settings for controls
#stepsize
step_max = 1.0
step_min = 0.1
step_step = 0.05
step_init = 1
#initial value
x0_max = 2.0
x0_min = 0.0
x0_step = 0.1
x0_init = 1.0
#ode solver
solver_init = 0
#ode type
odetype_init = 0


