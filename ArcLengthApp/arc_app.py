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
arc_settings = import_bokeh('arc_settings.py')
arc_functions = import_bokeh('arc_functions.py')

# initialize data source
source_curve = ColumnDataSource(data=dict(x=[], y=[]))
source_point = ColumnDataSource(data=dict(x=[], y=[]))
source_patches = ColumnDataSource(data=dict(xs=[], ys=[]))
source_segments = ColumnDataSource(data=dict(x0=[], y0=[], x1=[], y1=[]))

# initialize controls
# choose between original and arc length parametrization
parametrization_input = RadioButtonGroup(labels=['original','arc length'],active=0)
# slider controlling the current parameter t
t_value_input = Slider(title="parameter t", name='parameter t', value=arc_settings.t_value_init,
                       start=arc_settings.t_value_min, end=arc_settings.t_value_max,
                       step=arc_settings.t_value_step)
# text input for the x component of the curve
x_component_input = TextInput(value=arc_settings.x_component_input_msg, title="curve x")
# text input for the y component of the curve
y_component_input = TextInput(value=arc_settings.y_component_input_msg, title="curve y")


def update_curve():
    # parse x and y component
    f_x = arc_functions.parser(x_component_input.value)
    f_y = arc_functions.parser(y_component_input.value)

    t = np.linspace(arc_settings.t_value_min, arc_settings.t_value_max, arc_settings.resolution) # evaluation interval

    x = f_x(t)
    y = f_y(t)

    # saving data to plot
    source_curve.data = dict(x=x, y=y)


def get_parameter(parametrization_type):
    if parametrization_type == 0: # normal parametrization
        # Get the current slider value
        t0 = t_value_input.value
    elif parametrization_type == 1: # arc length parametrization
        f_x_str = x_component_input.value
        f_y_str = y_component_input.value
        f_x_sym = arc_functions.sym_parser(f_x_str)
        f_y_sym = arc_functions.sym_parser(f_y_str)
        from sympy.core import diff
        df_x_sym = diff(f_x_sym)
        df_y_sym = diff(f_y_sym)
        from sympy.abc import t
        from sympy import lambdify
        df_x = lambdify(t, df_x_sym, ['numpy'])
        df_y = lambdify(t, df_y_sym, ['numpy'])
        # compute arc length
        arc_length = arc_functions.arclength(df_x,df_y,arc_settings.t_value_max)
        # map input interval [t_value_min,t_value_max] to [0,arc_length]
        width_t = (arc_settings.t_value_max-arc_settings.t_value_min)
        t_fraction = (t_value_input.value - arc_settings.t_value_min)/ width_t
        t_arc_length = t_fraction * arc_length
        # compute corresponding value on original parametrization
        t0 = arc_functions.s_inverse(df_x,df_y,t_arc_length)

    return t0

def update_point():
    # Get the current slider value
    parametrization_type = parametrization_input.active
    t0 = get_parameter(parametrization_type)

    f_x_str = x_component_input.value
    f_y_str = y_component_input.value
    f_x = arc_functions.parser(f_x_str)
    f_y = arc_functions.parser(f_y_str)

    x0 = f_x(t0)
    y0 = f_y(t0)

    # saving data to plot
    source_point.data = dict(x=[x0], y=[y0])


def update_tangent():
    parametrization_type = parametrization_input.active
    t0 = get_parameter(parametrization_type)

    f_x_str = x_component_input.value
    f_y_str = y_component_input.value

    x,y,u,v = arc_functions.calculate_tangent(f_x_str, f_y_str, t0)

    if parametrization_type == 1: # arc length parametrization
        u,v = arc_functions.normalize(u,v)

    segments, patches = arc_functions.calculate_arrow_data(x,y,u,v)

    source_segments.data = segments
    source_patches.data = patches


def curve_change(attrname, old, new):
    update_curve()
    update_point()
    update_tangent()

def t_value_change(attrname, old, new):
    update_point()
    update_tangent()

def parametrization_change(self):
    update_point()
    update_tangent()


# setup events
t_value_input.on_change('value', t_value_change)
x_component_input.on_change('value', curve_change)
y_component_input.on_change('value', curve_change)
parametrization_input.on_click(parametrization_change)

# initialize plot
toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt", plot_height=400, plot_width=400, tools=toolset,
              title="Arc length parametrization",
              x_range=[arc_settings.x_min_view, arc_settings.x_max_view],
              y_range=[arc_settings.y_min_view, arc_settings.y_max_view])

# Plot the line by the x,y values in the source property
plot.line('x', 'y', source=source_curve, line_width=3, line_alpha=1, color='black', legend='curve')
plot.scatter('x', 'y', source=source_point, color='blue', legend='point at t')

# Plot Tangent
plot.segment('x0', 'y0', 'x1', 'y1', source=source_segments)
plot.patches('xs', 'ys', source=source_patches)

# calculate data
update_curve()
update_point()
update_tangent()

# lists all the controls in our app
controls = VBoxForm(children=[parametrization_input,t_value_input,HBox(width=400,children=[x_component_input, y_component_input])])

# make layout
curdoc().add_root(VBox(children=[plot, controls]))