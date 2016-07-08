from __future__ import division

import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from bokeh.models import ColumnDataSource, Slider
from bokeh.layouts import widgetbox, row, column, Spacer
from bokeh.plotting import Figure
from bokeh.io import curdoc

def callback_function(attrname, old_N, new_N):

    t = slider.value
    m = .5
    x = np.array(plot_data.data['x'])
    y = m*x+t
    plot_data.data = dict(x=x.tolist(),y=y.tolist())


def init():
    t = slider.value
    m = .5
    x = np.linspace(0,1)
    y = m*x+t
    plot_data.data = dict(x=x.tolist(),y=y.tolist())



# initialize data source
plot_data = ColumnDataSource(data=dict(x=[], y=[]))

# initialize controls
slider = Slider(title="a", name='a', value=.5, start=0, end=1,
                     step=.1)
slider.on_change('value', callback_function)

# initialize plot
toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
# Generate a figure container
plot = Figure(plot_height=400,
              plot_width=400,
              tools=toolset,
              title="Time dependent PDEs",
              x_range=[0,1],
              y_range=[0,1]
              )

# Plot the numerical solution at time=t by the x,u values in the source property
plot.line('x', 'y', source=plot_data,
          line_width=.5,
          line_alpha=.6,
          line_dash=[4, 4],
          color='red')
# calculate data
init()

# lists all the controls in our app
controls = widgetbox(slider,width=400)

# make layout
curdoc().add_root(row(plot,controls,width=800))