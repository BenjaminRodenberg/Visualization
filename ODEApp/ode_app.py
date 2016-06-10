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
    return imp.load_source('', app_root_dir+'/'+relative_path)
# import local modules
ode_fun = import_bokeh('ode_functions.py')
ode_settings = import_bokeh('ode_settings.py')

logging.basicConfig(level=logging.DEBUG)

# initialize data source
source_num = ColumnDataSource(data=dict(t_num=[], x_num=[]))
source_ref = ColumnDataSource(data=dict(t_ref=[], x_ref=[]))

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


# todo refactor! BLOB
def update_data(attrname, old, new):
    # default values for ODEs...
    timespan = ode_settings.max_time
    # available ODEs
    ode_library = ode_settings.ode_library
    # respective reference solutions
    ref_library = ode_settings.ref_library
    # available solvers
    solver_library = ode_settings.solver_library

    # Get the current slider values
    h = stepsize.value
    x0 = startvalue.value
    solver = solver_library[solvers.active]
    ode = ode_library[odes.active]
    ref = ref_library[odes.active]

    if odes.active == 3:
        x0 = np.array([x0,0])
    else:
        x0 = np.array([x0])

    # solve ode with numerical scheme
    [t_num, x_num] = solver(ode, x0, h, timespan)
    [t_ref, x_ref] = ode_fun.ref_sol(ref, x0, timespan)
    # save data
    x_num = x_num[0,:] # only take first line of solutions
    x_num = x_num.tolist()
    t_num = t_num.tolist()
    x_ref = x_ref.tolist()
    t_ref = t_ref.tolist()
    # save lists to data sources
    source_num.data = dict(x_num=x_num, t_num=t_num)
    source_ref.data = dict(x_ref=x_ref, t_ref=t_ref)

    print "data was updated with parameters: h=" + str(h) + " and x0=" + str(x0)


def init_data():
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
plot.circle('t_num','x_num', source=source_num,
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
    children=[VBox(height=100),stepsize, startvalue, HBox(children=[solvers],width=400), HBox(children=[odes],width=400)],
    width=350
)

# make layout
curdoc().add_root(HBox(children=[plot, controls],width=750))