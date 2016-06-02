"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""
# ==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
# ==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import Slider, HBox, VBoxForm, TextInput, Panel, Tabs, Dropdown, VBoxForm, VBox
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure
from bokeh.io import curdoc, vform

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
odesystem_settings = import_bokeh('odesystem_settings.py')
odesystem_helpers = import_bokeh('odesystem_helpers.py')
my_bokeh_utils = import_bokeh('../my_bokeh_utils.py')

# initialize data source
source_patches = ColumnDataSource(data=dict(xs=[], ys=[]))  # patches defining the arrow tips of the quiver plot
source_segments = ColumnDataSource(data=dict(x0=[], y0=[], x1=[], y1=[]))  # segments defining the arrow lines of the quiver plot
source_basept = ColumnDataSource(data=dict(x=[], y=[]))  # points lying in the middle of each arrow defining the point the arrow is referring to
source_streamline = ColumnDataSource(data=dict(x=[], y=[]))  # streamline data
source_initialvalue = ColumnDataSource(data=dict(x0=[], y0=[]))  # initial value data (only one point)
source_critical_pts = ColumnDataSource(data=dict(x=[], y=[]))  # critical point data (multiple points)
source_critical_lines = ColumnDataSource(data=dict(x_ls=[[]], y_ls=[[]]))  # critical line data (multiple sets of points connecting to lines)
source_view = ColumnDataSource(data=dict(x_start=[odesystem_settings.x_min],
                                         x_end=[odesystem_settings.x_max],
                                         y_start=[odesystem_settings.y_min],
                                         y_end=[odesystem_settings.y_max]))  # user view information


def init_data():
    """
    initializes the data.
    1. get the ode function components u and v
    2. get the initial value for the streamline
    3. compute quiver and streamline
    :return:
    """
    u_str = u_input.value
    v_str = v_input.value
    x0 = x0_input.value
    y0 = y0_input.value
    update_quiver_data(u_str, v_str)
    update_streamline_data(u_str, v_str, x0, y0)


def ode_change(attrname, old, new):
    """
    called, if the ode changes, i.e. one of the function u or v is modified. If the ode changes the quiver field as well
    as the streamline change. Additionally the global boolean value update_callback has to be set (this value is used
    for preventing unnecessary computation if both u and v are changed at the same time).
    :param attrname:
    :param old:
    :param new:
    :return:
    """
    global update_callback
    if update_callback:
        u_str = u_input.value
        v_str = v_input.value
        x0 = x0_input.value
        y0 = y0_input.value
        update_quiver_data(u_str, v_str)
        update_streamline_data(u_str, v_str, x0, y0)


def initial_value_change(attrname, old, new):
    """
    called, if the initial value for the streamline changes. The streamline has to by recomputed.
    :param attrname:
    :param old:
    :param new:
    :return:
    """
    u_str = u_input.value
    v_str = v_input.value
    x0 = x0_input.value
    y0 = y0_input.value
    update_streamline_data(u_str, v_str, x0, y0)


def get_plot_bounds(plot):
    """
    helper function returning the bounds of the plot in a dict.
    :param plot: handle to the bokeh.plotting.Figure
    :return:
    """
    x_min = plot.x_range.start
    x_max = plot.x_range.end
    y_min = plot.y_range.start
    y_max = plot.y_range.end
    return {'x_min':x_min,
            'x_max':x_max,
            'y_min':y_min,
            'y_max':y_max}


def update_streamline_data(u_str, v_str, x0, y0):
    """
    updates the bokeh.models.ColumnDataSource holding the streamline data.
    :param u_str: string, first component of the ode
    :param v_str: string, second component of the ode
    :param x0: initial value x for the streamline
    :param y0: initial value y for the streamline
    :return:
    """
    # string parsing
    u_fun, u_sym = odesystem_helpers.parser(u_str)
    v_fun, v_sym = odesystem_helpers.parser(v_str)
    # numerical integration
    chaotic = (sample_fun_input.value == "dixon") # for the dixon system a special treatment is necessary
    x_val, y_val = odesystem_helpers.do_integration(x0, y0, u_fun, v_fun, get_plot_bounds(plot), chaotic)
    # update sources
    streamline_to_data(x_val, y_val, x0, y0) # save data to ColumnDataSource
    print "streamline was calculated for initial value (x0,y0)=(%f,%f)" % (x0, y0)


def update_quiver_data(u_str, v_str):
    """
    updates the bokeh.models.ColumnDataSource_s holding the quiver data and the ciritical points and lines of the ode.
    :param u_str: string, first component of the ode
    :param v_str: string, second component of the ode
    :return:
    """
    # string parsing
    u_fun, u_sym = odesystem_helpers.parser(u_str)
    v_fun, v_sym = odesystem_helpers.parser(v_str)
    # compute critical points
    x_c, y_c, x_lines, y_lines = odesystem_helpers.critical_points(u_sym, v_sym, get_plot_bounds(plot))
    # crating samples
    x_val, y_val, u_val, v_val, h = get_samples(u_fun, v_fun)
    # generating quiver data and updating sources
    ssdict, spdict, sbdict = my_bokeh_utils.quiver_to_data(x_val, y_val, u_val, v_val, h)
    # save quiver data to respective ColumnDataSource_s
    source_segments.data = ssdict
    source_patches.data = spdict
    source_basept.data = sbdict
    # save critical point data
    critical_to_data(x_c, y_c, x_lines, y_lines)

    print "quiver data was updated for u(x,y) = %s, v(x,y) = %s" % (u_str, v_str)


def get_samples(u_fun, v_fun):
    """
    compute sample points where the ode is evaluated.
    :param u_fun: function handle, first component of the ode
    :param v_fun: function handle, second component of the ode
    :return:
    """
    # compute distance of sample points
    h = odesystem_helpers.get_stepwidth(source_view.data['x_start'][0], source_view.data['x_end'][0])
    # create a grid of samples
    xx = np.arange(source_view.data['x_start'][0], source_view.data['x_end'][0], h)
    yy = np.arange(source_view.data['y_start'][0], source_view.data['y_end'][0], h)
    x_val, y_val = np.meshgrid(xx, yy)
    # initialize arrays
    v_val = np.empty(x_val.shape)
    u_val = np.empty(x_val.shape)
    # evaluate ode at sample points
    for i in range(x_val.shape[0]):
        for j in range(x_val.shape[1]):
            v_val[i, j] = v_fun(x_val[i, j], y_val[i, j])
            u_val[i, j] = u_fun(x_val[i, j], y_val[i, j])

    return x_val, y_val, u_val, v_val, h


def streamline_to_data(x_val, y_val, x0, y0):
    """
    save streamline to bokeh.models.ColumnDataSource
    :param x_val: streamline data x
    :param y_val: streamline data y
    :param x0: initial value x of streamline
    :param y0: initial value y of streamline
    :return:
    """
    source_initialvalue.data = dict(x0=[x0], y0=[y0])
    source_streamline.data = dict(x=x_val, y=y_val)


def critical_to_data(x_c, y_c, x_lines, y_lines):
    """
    save critical points and lines to bokeh.models.ColumnDataSource
    :param x_c: critical points x
    :param y_c: critical points y
    :param x_lines: set of lines (multiple points x)
    :param y_lines: set of lines (multiple points y)
    :return:
    """
    source_critical_pts.data = dict(x=x_c, y=y_c)
    source_critical_lines.data = dict(x_ls=x_lines, y_ls=y_lines)


# initialize controls
# text input for input of the ode system [u,v] = [x',y']
u_input = TextInput(value=odesystem_settings.sample_system_functions[odesystem_settings.init_fun_key][0], title="u(x,y):")
v_input = TextInput(value=odesystem_settings.sample_system_functions[odesystem_settings.init_fun_key][1], title="v(x,y):")

# slider input for initial value [x,y](t=0) = [x0,y0]
x0_input = Slider(title="x0",
                  value=odesystem_settings.x0_input_init,
                  start=odesystem_settings.x_min,
                  end=odesystem_settings.x_max,
                  step=odesystem_settings.x0_step)
y0_input = Slider(title="y0",
                  value=odesystem_settings.y0_input_init,
                  start=odesystem_settings.y_min,
                  end=odesystem_settings.y_max,
                  step=odesystem_settings.y0_step)

# dropdown menu for selecting one of the sample functions
sample_fun_input = Dropdown(label="choose a sample function pair or enter one below",
                            menu=odesystem_settings.sample_system_names)


def sample_fun_change(self):
    """
    called if the sample function is changed. The global variable update_callback is used to prevent triggering the
    callback function ode_change twice, once for change in u with old v, then for change in v with new u.
    :param self:
    :return:
    """
    global update_callback
    # get sample function pair (first & second component of ode)
    sample_fun_key = sample_fun_input.value
    sample_fun_u, sample_fun_v = odesystem_settings.sample_system_functions[sample_fun_key]
    # write new functions to u_input and v_input
    update_callback = False  # prevent callback
    u_input.value = sample_fun_u
    update_callback = True  # allow callback
    v_input.value = sample_fun_v


# initialize callback behaviour
sample_fun_input.on_click(sample_fun_change)
u_input.on_change('value', ode_change)
v_input.on_change('value', ode_change)
x0_input.on_change('value', initial_value_change)
y0_input.on_change('value', initial_value_change)

# initialize plot
toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt",
              plot_height=400,
              plot_width=400,
              tools=toolset,
              title="2D ODE System",
              x_range=[odesystem_settings.x_min, odesystem_settings.x_max],
              y_range=[odesystem_settings.y_min, odesystem_settings.y_max]
              )
# remove grid from plot
plot.grid[0].grid_line_alpha = 0.0
plot.grid[1].grid_line_alpha = 0.0

# Plot the direction field
plot.segment('x0', 'y0', 'x1', 'y1', source=source_segments)
plot.patches('xs', 'ys', source=source_patches)
plot.circle('x', 'y', source=source_basept, color='blue', size=1.5)
# Plot initial values
plot.scatter('x0', 'y0', source=source_initialvalue, color='black', legend='(x0,y0)')
# Plot streamline
plot.line('x', 'y', source=source_streamline, color='black', legend='streamline')
# Plot critical points and lines
plot.scatter('x', 'y', source=source_critical_pts, color='red', legend='critical pts')
plot.multi_line('x_ls', 'y_ls', source=source_critical_lines, color='red', legend='critical lines')


def refresh_quiver():
    """
    periodically called function that updates data with respect to the current user view, if the user view has changed.
    :return:
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot)
    if user_view_has_changed:
        u_str = u_input.value
        v_str = v_input.value
        update_quiver_data(u_str, v_str)
        source_view.data = my_bokeh_utils.get_user_view(plot)


# calculate data
init_data()

# lists all the controls in our app associated with the default_funs panel
ww=400
function_controls = VBoxForm(
    children=[sample_fun_input,VBox(width=ww,height=20), u_input, v_input,VBox(width=ww,height=20)],
    width=ww)
streamline_controls = VBoxForm(
    children=[VBox(width=ww,height=50),x0_input, y0_input,VBox(width=ww,height=10)],
    width=ww)

# Panels for sample functions or default functions
function_panel = Panel(child=function_controls, title='choose function')
streamline_panel = Panel(child=streamline_controls, title='modify streamline')
# Add panels to tabs
tabs = VBox(
    children=[Tabs(tabs=[function_panel, streamline_panel])],
    width=ww)

# refresh quiver field all 100ms
curdoc().add_periodic_callback(refresh_quiver, 100)
# make layout
curdoc().add_root(VBoxForm(children=[HBox(children=[plot, tabs])]))