# ==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
# ==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import VBox, Slider, RadioButtonGroup, VBoxForm, HBox, Dropdown, TextInput
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure
from bokeh.io import curdoc

import numpy as np

# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
leibnitz_settings = import_bokeh('leibnitz_settings.py')
lf = import_bokeh('leibnitz_functions.py')

# initialize data source
source_curve = ColumnDataSource(data=dict(x=[], y=[]))
source_point = ColumnDataSource(data=dict(x=[], y=[]))
source_sector = ColumnDataSource(data=dict(x=[], y=[]))
source_lines = ColumnDataSource(data=dict(x_start=[], y_start=[], x_end=[], y_end=[]))

# initialize controls
# slider controlling the current parameter t
t_value_input = Slider(title="parameter t", name='parameter t', value=leibnitz_settings.t_value_init,
                       start=leibnitz_settings.t_value_min, end=leibnitz_settings.t_value_max,
                       step=leibnitz_settings.t_value_step)
# text input for the x component of the curve
x_component_input = TextInput(value=leibnitz_settings.x_component_input_msg, title="curve x")
# text input for the y component of the curve
y_component_input = TextInput(value=leibnitz_settings.y_component_input_msg, title="curve y")


def update_curve():
    # parse x and y component
    f_x = lf.parser(x_component_input.value)
    f_y = lf.parser(y_component_input.value)

    t = np.linspace(leibnitz_settings.t_value_min, leibnitz_settings.t_value_max, leibnitz_settings.resolution) # evaluation interval

    x = f_x(t)
    y = f_y(t)

    # saving data to plot
    source_curve.data = dict(x=x, y=y)


def update_point():
    # Get the current slider value
    t0 = t_value_input.value
    f_x = lf.parser(x_component_input.value)
    f_y = lf.parser(y_component_input.value)

    t_min = leibnitz_settings.t_value_min

    t = np.linspace(t_min , t0,
                    leibnitz_settings.resolution)  # evaluation interval

    x = f_x(t)
    y = f_y(t)

    x = np.array([0] + x.tolist() + [0])
    y = np.array([0] + y.tolist() + [0])

    x0 = f_x(t0)
    y0 = f_y(t0)

    # saving data to plot
    source_point.data = dict(x=[x0], y=[y0])
    source_sector.data = dict(x=x,y=y)
    source_lines.data = dict(x_start=[0,f_x(t_min)], y_start=[0,f_y(t_min)],
                             x_end = [0,f_x(t0)], y_end=[0,f_y(t0)])


def curve_change(attrname, old, new):
    update_curve()
    update_point()

def t_value_change(attrname, old, new):
    update_point()


# setup events
t_value_input.on_change('value', t_value_change)
x_component_input.on_change('value', curve_change)
y_component_input.on_change('value', curve_change)

# initialize plot
toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt", plot_height=400, plot_width=400, tools=toolset,
              title="Leibnitz sector formula",
              x_range=[leibnitz_settings.x_min_view, leibnitz_settings.x_max_view],
              y_range=[leibnitz_settings.y_min_view, leibnitz_settings.y_max_view])

# Plot the line by the x,y values in the source property
plot.line('x', 'y', source=source_curve, line_width=3, line_alpha=1, color='black', legend='curve')
plot.scatter('x', 'y', source=source_point, color='blue', legend='point at t')
plot.scatter([0],[0], color='black', marker='x')
pat = plot.patch('x', 'y', source=source_sector, fill_color='blue', fill_alpha=.2, legend='area')
plot.line('x_start', 'y_start', source=source_lines, line_width=1, line_alpha=1, color='blue')
plot.line('x_end', 'y_end', source=source_lines, line_width=1, line_alpha=1, color='blue')

# calculate data
update_curve()
update_point()

# lists all the controls in our app
controls = VBoxForm(children=[t_value_input,HBox(width=400,children=[x_component_input, y_component_input])])

# make layout
curdoc().add_root(VBox(children=[plot, controls]))