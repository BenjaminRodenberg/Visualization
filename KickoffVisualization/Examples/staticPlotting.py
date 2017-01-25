import numpy as np
from bokeh.plotting import figure, show, output_file

# create data
x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)
# define tools
TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
# plot data
p1 = figure(title="Legend Example", tools=TOOLS)
p1.circle(x,   y, legend="sin(x)")
p1.circle(x, 2*y, legend="5*sin(x)", color="blue")
p1.circle(x, 3*y, legend="3*sin(x)", color="green")
# save and open plot
output_file("legend.html", title="legend.py example")
show(p1)