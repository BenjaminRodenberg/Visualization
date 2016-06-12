x_min = -1
x_max = +1
y_min = -1
y_max = +1
res_x = 400
res_y = res_x
sq_size = 10

f_init = "x ** 2 + y ** 3"
g_init = "x ** 2 + y ** 2 - 1"

# list defining the dropdown menu.
# the tuples have the following meaning: (<name in dropdown menu>, <key for sample_system_functions>)
sample_f_names = [
    ("polynomial", "polynomial"),
    ("distance from origin", "distance_origin"),
    ("distance from (1,1)", "distance_point")
]

sample_g_names = [
    ("circle", "circle"),
    ("ellipsis", "ellipsis"),
    ("sin curve", "sin_curve"),
    ("hyperbola", "hyperbola")
]
# key value pairs holding the with the function pair (u,v) that defines the ode system
sample_functions_f = {
    "polynomial":"4*x^2-3*x*y",
    "distance_origin":"x^2+y^2",
    "distance_point":"(x-1)^2+(y-1)^2"
}

sample_functions_g = {
    "circle":"x^2+y^2-1",
    "ellipsis": "x^2+4*y^2-1",
    "sin_curve": "sin(x)-y",
    "hyperbola": "x^2-y^2-1/4"
}