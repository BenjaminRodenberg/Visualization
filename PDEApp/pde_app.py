"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

from __future__ import division

import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from bokeh.models.widgets import HBox, Slider, RadioButtonGroup, VBoxForm, TextInput
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure
from bokeh.io import curdoc

# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
pde_settings = import_bokeh('pde_settings.py')
pde_functions = import_bokeh('pde_functions.py')

# initialize data source
plot_data_num = ColumnDataSource(data=dict(x=[], u=[]))
plot_data_ana = ColumnDataSource(data=dict(x=[],u=[]))
mesh_data = ColumnDataSource(data=dict())
pde_specs = ColumnDataSource(data=dict(h=[], k=[]))

# initialize controls
# slider for going though time
time_slider = Slider(title="time", name='time', value=pde_settings.t_init, start=pde_settings.t_min, end=pde_settings.t_max,
                     step=pde_settings.t_step)
# slider controlling spatial stepsize of the solver
h_slider = Slider(title="spatial meshwidth", name='spatial meshwidth', value=pde_settings.h_init, start=pde_settings.h_min,
                  end=pde_settings.h_max, step=pde_settings.h_step)
# slider controlling spatial stepsize of the solver
k_slider = Slider(title="temporal meshwidth", name='temporal meshwidth', value=pde_settings.k_init, start=pde_settings.k_min,
                  end=pde_settings.k_max, step=pde_settings.k_step)
# radiobuttons controlling pde type
pde_type = RadioButtonGroup(labels=['Heat', 'Wave'], active=0)
# radiobuttons controlling solver type
solver_type = RadioButtonGroup(labels=['Explicit', 'Implicit'], active=0)
# text input for IC
initial_condition = TextInput(value=pde_settings.IC_init, title="initial condition")


def get_num_data(k,t):
    idx = int(round(t / k, 0))
    u_key = 'u' + str(idx)
    x = mesh_data.data['x']
    u = mesh_data.data[u_key]
    return x, u


def get_ana_data(t):
    x = np.linspace(pde_settings.x_min, pde_settings.x_max, 100)
    u_ana_id = get_solver_id()
    f0 = pde_functions.parse(initial_condition.value)
    u = pde_settings.analytical_solutions[u_ana_id](f0, x, t)
    return x, u


def update_plot(k, t):
    x_num, u_num = get_num_data(k,t)
    x_ana, u_ana = get_ana_data(t)
    plot_data_num.data = dict(x=x_num, u=u_num)
    plot_data_ana.data = dict(x=x_ana, u=u_ana)


def get_solver_id():
    return pde_type.active * 2 + solver_type.active


def mesh_change(attrname, old, new):
    h = h_slider.value  # spatial meshwidth
    k = k_slider.value  # temporal meshwidth
    print "mesh changed to " + str((h, k))
    update_mesh(h, k)


def time_change(attrname, old, new):
    k = k_slider.value
    t = time_slider.value
    update_plot(k, t)
    print "new time: " + str(t)


def update_mesh(h, k):
    solver_id = get_solver_id()
    pde_specs.data = dict(h=[h], k=[k], solver_id=[solver_id])

    solver = pde_settings.solvers[solver_id]

    x0 = pde_settings.x_min
    x1 = pde_settings.x_max
    N = int(round((x1 - x0) / h + 1, 0))
    x = np.linspace(x0, x1, N)
    f0 = pde_functions.parse(initial_condition.value)
    u = f0(x)

    u_old = np.array(u)  # this enforces neumann BC: u'(t=0)=0

    M = int(round(pde_settings.t_max / k, 0)) + 1

    mesh_dict = dict(x=x)

    for i in range(M):
        key = 'u' + str(i)
        mesh_dict[key] = u.tolist()
        u_new = solver(u_old, u, k, h)
        u_old = u
        u = u_new

    mesh_data.data = mesh_dict
    t = time_slider.value
    update_plot(k, t)


def init_pde():
    h = h_slider.value
    k = k_slider.value
    update_mesh(h, k)

# event registration
time_slider.on_change('value', time_change)
h_slider.on_change('value', mesh_change)
k_slider.on_change('value', mesh_change)
solver_type.on_change('active', mesh_change)
pde_type.on_change('active', mesh_change)
initial_condition.on_change('value', mesh_change)

# initialize plot
toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt",
              plot_height=400,
              plot_width=400,
              tools=toolset,
              title="Time dependent PDEs",
              x_range=[pde_settings.x_min, pde_settings.x_max],
              y_range=[-1, 1]
              )

# Plot the numerical solution at time=t by the x,u values in the source property
plot.line('x', 'u', source=plot_data_num,
          line_width=.5,
          line_alpha=.6,
          line_dash=[4, 4],
          color='red')
plot.line('x', 'u', source=plot_data_ana,
          line_width=.5,
          line_alpha=.6,
          color='blue',
          legend='analytical solution')
plot.circle('x', 'u', source=plot_data_num,
            color='red',
            legend='numerical solution')

# calculate data
init_pde()

# lists all the controls in our app
controls = VBoxForm(children=[initial_condition,
                              time_slider,
                              h_slider,
                              k_slider,
                              HBox(children=[pde_type, solver_type],
                                   width=300)],
                    width=400)

# make layout
curdoc().add_root(HBox(children=[plot,controls],width=800))
