"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging
import numpy as np

from bokeh.models.widgets import HBox, VBox, Slider, RadioButtonGroup
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
ode_fun = import_bokeh('ode_functions.py')
ode_settings = import_bokeh('ode_settings.py')
my_bokeh_utils = import_bokeh('../my_bokeh_utils.py')

logging.basicConfig(level=logging.DEBUG)

# initialize data source
source_num = ColumnDataSource(data=dict(t_num=[], x_num=[]))
source_ref = ColumnDataSource(data=dict(t_ref=[], x_ref=[]))
source_view = ColumnDataSource(data=dict(x_start=[ode_settings.min_time],
                                         y_start=[ode_settings.min_y],
                                         x_end=[ode_settings.max_time],
                                         y_end=[ode_settings.max_y],
                                         ))

# initialize controls
# slider controlling stepsize of the solver
stepsize = Slider(title="stepsize", name='stepsize', value=ode_settings.step_init, start=ode_settings.step_min,
                  end=ode_settings.step_max, step=ode_settings.step_step)
# slider controlling initial value of the ode
startvalue = Slider(title="startvalue", name='startvalue', value=ode_settings.x0_init, start=ode_settings.x0_min,
                    end=ode_settings.x0_max, step=ode_settings.x0_step)
# gives the opportunity to choose from different solvers
solvers = RadioButtonGroup(labels=ode_settings.solver_labels, active=ode_settings.solver_init)
# gives the opportunity to choose from different odes
odes = RadioButtonGroup(labels=ode_settings.odetype_labels, active=ode_settings.odetype_init)


def compute_numerical_solution(ode_id, solver_id, x0, h):
    # get solver to be used
    solver = ode_settings.solver_library[solver_id]
    # get ode function handle
    ode = ode_settings.ode_library[ode_id]

    if odes.active == 3:  # special treatment for oszillator ode. Adding second component equal to zero.
        x0 = np.array([x0, 0])
    else:
        x0 = np.array([x0])

    t1 = source_view.data['x_end'][0]

    [t_num, x_num] = solver(ode, x0, h, t1)

    x_num = x_num[0, :]  # only take first line of solutions
    x_num = x_num.tolist()
    t_num = t_num.tolist()

    return dict(x_num=x_num, t_num=t_num)


def compute_reference_solution(ode_id, x0):
    # get reference solution function handle
    ref = ode_settings.ref_library[ode_id]

    t1 = source_view.data['x_end'][0]
    t0 = max([source_view.data['x_start'][0], 0])

    [t_ref, x_ref] = ode_fun.ref_sol(ref, x0, t_min=t0, t_max=t1, n_samples=1000)

    x_ref = x_ref.tolist()
    t_ref = t_ref.tolist()

    return dict(x_ref=x_ref, t_ref=t_ref)


def update_data(attrname, old, new):
    # update data sources
    source_num.data = compute_numerical_solution(odes.active, solvers.active, startvalue.value, stepsize.value)
    source_ref.data = compute_reference_solution(odes.active, startvalue.value)


def init_data():
    update_data(None, None, None)


def refresh_user_view():
    """
    periodically called function that updates data with respect to the current user view, if the user view has changed.
    :return:
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot)
    if user_view_has_changed:
        source_view.data = my_bokeh_utils.get_user_view(plot)
        update_data(None, None, None)


# event registration
stepsize.on_change('value', update_data)
startvalue.on_change('value', update_data)
solvers.on_change('active', update_data)
odes.on_change('active', update_data)

# initialize plot
toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt",
              plot_height=400,
              plot_width=400,
              tools=toolset,
              # title=text.value,
              title=ode_settings.title,
              x_range=[ode_settings.min_time, ode_settings.max_time],
              y_range=[ode_settings.min_y, ode_settings.max_y]
              )
# Plot the numerical solution by the x,t values in the source property
plot.line('t_num', 'x_num', source=source_num,
          line_width=.5,
          line_alpha=0.6,
          color='red',
          line_dash=[4, 4]
          )
plot.circle('t_num', 'x_num', source=source_num,
            color='red',
            legend='numerical solution'
            )
# Plot the analytical solution by the x_ref,t values in the source property
plot.line('t_ref', 'x_ref', source=source_ref,
          color='green',
          line_width=3,
          line_alpha=0.6,
          legend='analytical solution'
          )
# calculate data
init_data()

# lists all the controls in our app
controls = VBox(
    children=[VBox(height=100), stepsize, startvalue, HBox(children=[solvers], width=400),
              HBox(children=[odes], width=400)],
    width=350
)

curdoc().add_periodic_callback(refresh_user_view, 100)
# make layout
curdoc().add_root(HBox(children=[plot, controls], width=750))
