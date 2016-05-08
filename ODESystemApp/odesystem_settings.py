__author__ = 'benjamin'

sample_system_functions = {
    "linear_stable": ("-x", "-y"),
    "linear_unstable": ("+x", "+y"),
    "saddlepoint": ("-y", "-x"),
    "circular_stable": ("-y", "x-y/10"),
    "circular_critical": ("-y", "x"),
    "circular_unstable": ("-y", "x+y/10"),
    "non_linear": ("(x-1)*(y-1)", "(x+1)*(y+1)")
}

sample_system_names = [
    ("linear_stable", "linear_stable"),
    ("linear_unstable", "linear_unstable"),
    ("saddlepoint", "saddlepoint"),
    ("circular_stable", "circular_stable"),
    ("circular_critical", "circular_critical"),
    ("circular_unstable", "circular_unstable"),
    ("non_linear", "non_linear"),
]

u_input_init = "(-2*y-x)*x"
v_input_init = "(x+2)*2*x"

x_min = -5.0
x_max = +5.0
y_min = -5.0
y_max = +5.0

x0_input_init=-2.0
y0_input_init=0.5

x0_step=.1
y0_step=.1

n_sample = 21
resolution = (x_max - x_min) / (n_sample-1)

screen_resolution = .5

Tmax = 100.0
