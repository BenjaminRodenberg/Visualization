from bokeh import ...
import numpy as np
from sympy import sympify, lambdify, diff
...
# Data
line_source = ColumnDataSource(data=dict(x=[], y=[]))

# Controls
f_input = TextInput(value="sin(x)", title="f(x):")
derivative_input = Slider(title="n", value=1.0, start=0.0, end=5.0, step=1)
...
# Plotting
plot = Figure(...)
plot.line(x='x', y='y', source=line_source, ...)
plot.line(x='x', y='dy', source=line_source, ...)

#Callback
f_input.on_change('value', fun_change)
derivative_input.on_change('value', fun_change)

#Layout
curdoc().add_root(row(plot,column(f_input,derivative_input)))
