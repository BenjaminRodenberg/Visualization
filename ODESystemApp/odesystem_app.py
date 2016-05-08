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

from bokeh.models.widgets import Slider, VBox, HBox, TextInput, Panel, Tabs, Dropdown
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
odesystem_settings = import_bokeh('odesystem_settings.py')
odesystem_helpers = import_bokeh('odesystem_helpers.py')

# initialize data source
source_patches = ColumnDataSource(data=dict(xs=[], ys=[]))
source_segments = ColumnDataSource(data=dict(x0=[], y0=[], x1=[], y1=[]))
source_basept = ColumnDataSource(data=dict(x=[], y=[]))
source_streamline = ColumnDataSource(data=dict(x=[], y=[]))
source_initialvalue = ColumnDataSource(data=dict(x0=[], y0=[]))
source_critical_pts = ColumnDataSource(data=dict(x=[], y=[]))
source_critical_lines = ColumnDataSource(data=dict(x_ls=[[]], y_ls=[[]]))

def get_plot_bounds():
    x_min = plot.x_range.__getattribute__('start')
    x_max = plot.x_range.__getattribute__('end')
    y_min = plot.y_range.__getattribute__('start')
    y_max = plot.y_range.__getattribute__('end')
    return {'x_min':x_min,
            'x_max':x_max,
            'y_min':y_min,
            'y_max':y_max}

def init_data():
    u_str = u_input.value
    v_str = v_input.value
    x0 = x0_input.value
    y0 = y0_input.value
    update_quiver_data(u_str, v_str)
    update_streamline_data(u_str, v_str, x0, y0)


def ode_change(attrname, old, new):
    u_str = u_input.value
    v_str = v_input.value
    x0 = x0_input.value
    y0 = y0_input.value
    update_quiver_data(u_str, v_str)
    update_streamline_data(u_str, v_str, x0, y0)


def start_change(attrname, old, new):
    u_str = u_input.value
    v_str = v_input.value
    x0 = x0_input.value
    y0 = y0_input.value
    update_streamline_data(u_str, v_str, x0, y0)


def update_streamline_data(u_str, v_str, x0, y0):
    # string parsing
    u_fun, u_sym = odesystem_helpers.parser(u_str)
    v_fun, v_sym = odesystem_helpers.parser(v_str)
    # numerical integration
    x_val, y_val = odesystem_helpers.do_integration(x0, y0, u_fun, v_fun, odesystem_settings.Tmax, get_plot_bounds())
    # update sources
    streamline_to_data(x_val, y_val, x0, y0)
    print "streamline was calculated for initial value (x0,y0)=(%d,%d)" % (x0, y0)


def update_quiver_data(u_str, v_str):
    # string parsing
    u_fun, u_sym = odesystem_helpers.parser(u_str)
    v_fun, v_sym = odesystem_helpers.parser(v_str)
    x_c, y_c, x_lines, y_lines = odesystem_helpers.critical_points(u_sym, v_sym, get_plot_bounds())
    # crating samples
    x_val, y_val, u_val, v_val, h = get_samples(u_fun, v_fun)
    # generating quiver data and updating sources
    quiver_to_data(x_val, y_val, u_val, v_val, h)
    critical_to_data(x_c, y_c, x_lines, y_lines)

    print "quiver data was updated for u(x,y) = %s, v(x,y) = %s" % (u_str, v_str)


def quiver_to_data(x, y, u, v, h):
    def __normalize(u, v, h):
        length = np.sqrt(u ** 2 + v ** 2)
        u[length > 0] *= 1.0 / length[length > 0] * h * .9
        v[length > 0] *= 1.0 / length[length > 0] * h * .9
        u[length == 0] = 0
        v[length == 0] = 0
        return u, v

    def quiver_to_segments(x, y, u, v, h):
        x = x.flatten()
        y = y.flatten()
        u = u.flatten()
        v = v.flatten()

        u, v = __normalize(u, v, h)

        x0 = x - u * .5
        y0 = y - v * .5
        x1 = x + u * .5
        y1 = y + v * .5

        return x0, y0, x1, y1

    def quiver_to_arrowheads(x, y, u, v, h):

        def __t_matrix(translate_x, translate_y):
            return np.array([[1, 0, translate_x],
                             [0, 1, translate_y],
                             [0, 0, 1]])

        def __r_matrix(rotation_angle):
            c = np.cos(rotation_angle)
            s = np.sin(rotation_angle)
            return np.array([[c, -s, 0],
                             [s, +c, 0],
                             [0, +0, 1]])

        def __head_template(x0, y0, u, v, type_id, headsize):
            if type_id is 0:
                x_patch = 3 * [None]
                y_patch = 3 * [None]

                x1 = x0 + u
                x_patch[0] = x1
                x_patch[1] = x1 - headsize
                x_patch[2] = x1 - headsize

                y1 = y0 + v
                y_patch[0] = y1
                y_patch[1] = y1 + headsize / np.sqrt(3)
                y_patch[2] = y1 - headsize / np.sqrt(3)
            elif type_id is 1:
                x_patch = 4 * [None]
                y_patch = 4 * [None]

                x1 = x0 + u
                x_patch[0] = x1
                x_patch[1] = x1 - headsize
                x_patch[2] = x1 - headsize / 2
                x_patch[3] = x1 - headsize

                y1 = y0 + v
                y_patch[0] = y1
                y_patch[1] = y1 + headsize / np.sqrt(3)
                y_patch[2] = y1
                y_patch[3] = y1 - headsize / np.sqrt(3)
            else:
                raise Exception("unknown head type!")

            return x_patch, y_patch

        def __get_patch_data(x0, y0, u, v, headsize):

            def angle_from_xy(x, y):
                if x == 0:
                    return np.pi * .5 + int(y <= 0) * np.pi
                else:
                    if y >= 0:
                        if x > 0:
                            return np.arctan(y / x)
                        elif x < 0:
                            return -np.arctan(y / -x) + np.pi
                        else:
                            return 1.5 * np.pi
                    else:
                        if x > 0:
                            return -np.arctan(-y / x)
                        elif x < 0:
                            return np.arctan(-y / -x) + np.pi
                        else:
                            return .5 * np.pi

            angle = angle_from_xy(u, v)

            x_patch, y_patch = __head_template(x0, y0, u, v, type_id=0, headsize=headsize)

            T1 = __t_matrix(-x_patch[0], -y_patch[0])
            R = __r_matrix(angle)
            T2 = __t_matrix(x_patch[0], y_patch[0])
            T = T2.dot(R.dot(T1))

            for i in range(x_patch.__len__()):
                v_in = np.array([x_patch[i], y_patch[i], 1])
                v_out = T.dot(v_in)
                x_patch[i], y_patch[i], tmp = v_out

            return x_patch, y_patch

        x = x.flatten()
        y = y.flatten()
        u = u.flatten()
        v = v.flatten()

        u, v = __normalize(u, v, h)

        n_arrows = x.shape[0]
        xs = n_arrows * [None]
        ys = n_arrows * [None]

        headsize = .1 * h

        for i in range(n_arrows):
            x_patch, y_patch = __get_patch_data(x[i] - .5 * u[i], y[i] - .5 * v[i], u[i], v[i], headsize)
            xs[i] = x_patch
            ys[i] = y_patch

        return xs, ys

    x0, y0, x1, y1 = quiver_to_segments(x, y, u, v, h)
    ssdict = dict(x0=x0, y0=y0, x1=x1, y1=y1)
    source_segments.data = ssdict

    xs, ys = quiver_to_arrowheads(x, y, u, v, h)
    spdict = dict(xs=xs, ys=ys)
    source_patches.data = spdict

    sbdict = dict(x=x.flatten(), y=y.flatten())
    source_basept.data = sbdict


def get_samples(u_fun, v_fun):
    bounds = get_plot_bounds()
    h = odesystem_helpers.get_stepwidth(bounds)

    xx = np.arange(bounds['x_min'], bounds['x_max'], h)
    yy = np.arange(bounds['y_min'], bounds['y_max'], h)

    x_val, y_val = np.meshgrid(xx, yy)

    v_val = np.empty(x_val.shape)
    u_val = np.empty(x_val.shape)

    for i in range(x_val.shape[0]):
        for j in range(x_val.shape[1]):
            v_val[i, j] = v_fun(x_val[i, j], y_val[i, j])
            u_val[i, j] = u_fun(x_val[i, j], y_val[i, j])

    return x_val, y_val, u_val, v_val, h


def streamline_to_data(x_val, y_val, x0, y0):
    source_initialvalue.data = dict(x0=[x0], y0=[y0])
    source_streamline.data = dict(x=x_val, y=y_val)


def critical_to_data(x_c, y_c, x_lines, y_lines):
    print "line data:"
    print x_lines
    print y_lines
    print "point data:"
    print x_c
    print y_c
    source_critical_pts.data = dict(x=x_c, y=y_c)
    source_critical_lines.data = dict(x_ls=x_lines, y_ls=y_lines)


# initialize controls
# text input for input of the ode system [u,v] = [x',y']
u_input = TextInput(value=odesystem_settings.u_input_init, title="u(x,y):")
v_input = TextInput(value=odesystem_settings.v_input_init, title="v(x,y):")

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
    sample_fun_key = sample_fun_input.value
    sample_fun_u, sample_fun_v = odesystem_settings.sample_system_functions[sample_fun_key]
    u_input.value = sample_fun_u
    v_input.value = sample_fun_v


sample_fun_input.on_click(sample_fun_change)

u_input.on_change('value', ode_change)
v_input.on_change('value', ode_change)
x0_input.on_change('value', start_change)
y0_input.on_change('value', start_change)

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
plot.grid[0].grid_line_alpha = 0.0
plot.grid[1].grid_line_alpha = 0.0

# Plot the direction field
plot.segment('x0', 'y0', 'x1', 'y1', source=source_segments)
plot.patches('xs', 'ys', source=source_patches)
plot.circle('x', 'y', source=source_basept, color='blue', size=1.5)
plot.scatter('x0', 'y0', source=source_initialvalue, color='black', legend='(x0,y0)')
plot.line('x', 'y', source=source_streamline, color='black', legend='streamline')
plot.scatter('x', 'y', source=source_critical_pts, color='red', legend='critical pts')
plot.multi_line('x_ls', 'y_ls', source=source_critical_lines, color='red', legend='critical lines')

# calculate data
init_data()

# lists all the controls in our app associated with the default_funs panel
function_controls = VBox(children=[HBox(width=400,children=[sample_fun_input]),
                                   HBox(children=[VBox(width=180, children=[u_input]),
                                                  VBox(width=40),
                                                  VBox(width=180, children=[v_input])]),
                                   ])

streamline_controls = HBox(children=[VBox(width=180, children=[x0_input]),
                                     VBox(width=40),
                                     VBox(width=180, children=[y0_input])])

# Panels for sample functions or default functions
function_panel = Panel(child=function_controls, title='choose function')
streamline_panel = Panel(child=streamline_controls, title='modify streamline')
# Add panels to tabs
tabs = Tabs(tabs=[function_panel, streamline_panel])

# make layout
curdoc().add_root(VBox(children=[plot, tabs]))
