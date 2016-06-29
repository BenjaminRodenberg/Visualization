# ==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
# ==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import Slider, RadioButtonGroup, Dropdown, TextInput, CheckboxGroup, \
    Panel, Tabs
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import Figure
from bokeh.io import curdoc

import numpy as np

global update_callback
update_callback = True


# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
arc_settings = import_bokeh('arc_settings.py')
arc_functions = import_bokeh('arc_functions.py')
my_bokeh_utils = import_bokeh('../my_bokeh_utils.py')

# initialize data source
source_curve = ColumnDataSource(data=dict(x=[], y=[]))

# plotting for normal parametrization
source_point_normal = ColumnDataSource(data=dict(x=[], y=[]))

# plotting for arc length parametrization
source_point_arc = ColumnDataSource(data=dict(x=[], y=[]))

# initialize controls
# choose between original and arc length parametrization
parametrization_input = CheckboxGroup(labels=['show original parametrization',
                                              'show arc length parametrization'],
                                      active=[0, 1])
# slider controlling the current parameter t
t_value_input = Slider(title="parameter t", name='parameter t', value=arc_settings.t_value_init,
                       start=arc_settings.t_value_min, end=arc_settings.t_value_max,
                       step=arc_settings.t_value_step)
# text input for the x component of the curve
x_component_input = TextInput(value=arc_settings.x_component_input_msg, title="curve x")
# text input for the y component of the curve
y_component_input = TextInput(value=arc_settings.y_component_input_msg, title="curve y")
# dropdown menu for selecting one of the sample curves
sample_curve_input = Dropdown(label="choose a sample function pair or enter one below",
                              menu=arc_settings.sample_curve_names)


def update_curve():
    # parse x and y component
    f_x = arc_functions.parser(x_component_input.value)
    f_y = arc_functions.parser(y_component_input.value)

    t = np.linspace(arc_settings.t_value_min, arc_settings.t_value_max, arc_settings.resolution)  # evaluation interval

    x = f_x(t)
    y = f_y(t)

    # saving data to plot
    source_curve.data = dict(x=x, y=y)


def get_parameter(parametrization_type):
    if parametrization_type == 0:  # normal parametrization
        # Get the current slider value
        t0 = t_value_input.value
    elif parametrization_type == 1:  # arc length parametrization
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
        arc_length = arc_functions.arclength(df_x, df_y, arc_settings.t_value_max)
        # map input interval [t_value_min,t_value_max] to [0,arc_length]
        width_t = (arc_settings.t_value_max - arc_settings.t_value_min)
        t_fraction = (t_value_input.value - arc_settings.t_value_min) / width_t
        t_arc_length = t_fraction * arc_length
        # compute corresponding value on original parametrization
        t0 = arc_functions.s_inverse(df_x, df_y, t_arc_length)

    return t0


def update_points():
    source_point_normal.data = dict(x=[], y=[])
    source_point_arc.data = dict(x=[], y=[])
    for i in parametrization_input.active:
        if i == 0:
            source_point_normal.data = update_point(0)
        elif i == 1:
            source_point_arc.data = update_point(1)


def update_point(parametrization_type):
    t0 = get_parameter(parametrization_type)

    f_x_str = x_component_input.value
    f_y_str = y_component_input.value
    f_x = arc_functions.parser(f_x_str)
    f_y = arc_functions.parser(f_y_str)

    x0 = f_x(t0)
    y0 = f_y(t0)

    point_dict = dict(x=[x0], y=[y0])

    return point_dict


def update_tangents():
    for i in parametrization_input.active:
        if i == 0:
            update_tangent(0)
        elif i == 1:
            update_tangent(1)


def update_tangent(parametrization_type):
    t0 = get_parameter(parametrization_type)

    f_x_str = x_component_input.value
    f_y_str = y_component_input.value

    x, y, u, v = arc_functions.calculate_tangent(f_x_str, f_y_str, t0)

    if parametrization_type == 1:  # arc length parametrization
        quiver[parametrization_type].compute_quiver_data(x, y, u, v, normalize=True)
    elif parametrization_type == 0:
        quiver[parametrization_type].compute_quiver_data(x, y, u, v, normalize=False)


def sample_curve_change(self):
    global update_callback
    # get sample function pair (first & second component of ode)
    sample_curve_key = sample_curve_input.value
    sample_curve_x_component, sample_curve_y_component = arc_settings.sample_curves[sample_curve_key]
    # write new functions to u_input and v_input
    update_callback = False  # prevent callback
    x_component_input.value = sample_curve_x_component
    update_callback = True  # allow callback
    y_component_input.value = sample_curve_y_component


def curve_change(attrname, old, new):
    global update_callback
    if update_callback:
        update_curve()
        update_points()
        update_tangents()


def t_value_change(attrname, old, new):
    update_points()
    update_tangents()


def parametrization_change(self):
    update_points()
    update_tangents()


# setup events
t_value_input.on_change('value', t_value_change)
x_component_input.on_change('value', curve_change)
y_component_input.on_change('value', curve_change)
parametrization_input.on_click(parametrization_change)
sample_curve_input.on_click(sample_curve_change)

# initialize plot
toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt", plot_height=400, plot_width=400, tools=toolset,
              title="Arc length parametrization",
              x_range=[arc_settings.x_min_view, arc_settings.x_max_view],
              y_range=[arc_settings.y_min_view, arc_settings.y_max_view])

# Plot the line by the x,y values in the source property
plot.line('x', 'y', source=source_curve, line_width=3, line_alpha=1, color='black', legend='curve')
# quiver related to normal length parametrization
quiver = 2*[None]
quiver[0] = my_bokeh_utils.Quiver(plot, fix_at_middle=False, line_width=2, color='blue')
plot.scatter('x', 'y', source=source_point_normal, color='blue', legend='original parametrization')
# quiver related to arc length parametrization
quiver[1] = my_bokeh_utils.Quiver(plot, fix_at_middle=False, line_width=2, color='red')
plot.scatter('x', 'y', source=source_point_arc, color='red', legend='arc length parametrization')

# calculate data
update_curve()
update_points()
update_tangents()

# make layout
curdoc().add_root(row(plot, widgetbox(parametrization_input, t_value_input, sample_curve_input, x_component_input,
                                      y_component_input, width=400)))
