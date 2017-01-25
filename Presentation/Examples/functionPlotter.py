from bokeh.models import ColumnDataSource, TextInput, Slider
from bokeh.layouts import column, row
from bokeh.plotting import Figure
from bokeh.io import curdoc

import numpy as np
from sympy import sympify, lambdify, diff

def sym_to_function_parser(fun_sym, args):
    if fun_sym.is_constant():
        fun_lam = lambda *x: np.ones_like(x[0]) * float(fun_sym)
    else:
        fun_lam = lambdify(args, fun_sym, modules=['numpy'])

    return fun_lam

def string_to_function_parser(fun_str, args):
    fun_sym = sympify(fun_str)
    fun_lam = sym_to_function_parser(fun_sym, args)
    return fun_lam, fun_sym

# Data
line_source = ColumnDataSource(data=dict(x=[], y=[]))

# Controls
f_input = TextInput(value="sin(x)", title="f(x):")
derivative_input = Slider(title="n", value=1.0, start=0.0, end=5.0, step=1)

def fun_change(attrname, old, new):
    f_str = f_input.value
    f_fun, f_sym = string_to_function_parser(f_str, ['x'])

    print derivative_input.value

    df_sym = diff(f_sym, 'x', int(derivative_input.value))
    df_fun = sym_to_function_parser(df_sym,['x'])
    x = np.linspace(-5, 5, 100)
    y = f_fun(x)
    dy = df_fun(x)

    line_source.data = dict(x=x, y=y, dy=dy)

def init_data():
    fun_change(None,None,None)

# Plotting
plot = Figure(title="function plotter",
              x_range=[-5,5],
              y_range=[-5,5])
plot.line(x='x', y='y', source=line_source, color='red', legend='f(x)')
plot.line(x='x', y='dy', source=line_source, color='blue', legend='df^n(x)')

#Callback
f_input.on_change('value', fun_change)
derivative_input.on_change('value', fun_change)

init_data()

#Layout
curdoc().add_root(row(plot,column(f_input,derivative_input)))
