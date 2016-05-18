from __future__ import division

import logging
import numpy as np

from bokeh.models.widgets import VBox, Button, Slider
from bokeh.models import ColumnDataSource, Callback
from bokeh.plotting import Figure
from bokeh.io import curdoc


# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir+'/'+relative_path)
# import local modules
mandel = import_bokeh('mandel.py')
mandel_colormap = import_bokeh('mandel_colormap.py')

logging.basicConfig(level=logging.DEBUG)

# initialize data source
source_image = ColumnDataSource(data=dict(image=[], x0=[None], y0=[None], xw=[None], yw=[None], max_iter=[None], freq=[None]))
source_its = ColumnDataSource(data=dict(its=[]))

# initialize controls
max_iter = Slider(title="iterations", name='iterations', value=50,
                 start=0, end=2000,
                 step=50)
freq = Slider(title="coloring", name='coloring', value=.5,
                 start=1, end=10,
                 step=1)

# initialize plot
toolset = "pan,reset,wheel_zoom,save"
# Generate a figure container
plot = Figure(title_text_font_size="12pt",
              plot_height=400,
              plot_width=400,
              x_range=[-2, 1],
              y_range=[-1.5, 1.5],
              tools=toolset,
              title="Mandelbrot Set"
              )
# Plot the mandelbrot set
plot.image_rgba(image='image',
                x='x0',
                y='y0',
                dw='xw',
                dh='yw',
                source=source_image)

from bokeh.models import NumeralTickFormatter, PrintfTickFormatter
# Turn off tick labels
plot.axis.formatter = PrintfTickFormatter(format=" ")
plot.axis.major_tick_line_color = None
plot.axis.minor_tick_line_color = None

def update_image(attrname, old, new):
    iterations = source_its.data['its'][0]

    x0 = plot.x_range.__getattribute__('start')
    y0 = plot.y_range.__getattribute__('start')
    xw = plot.x_range.__getattribute__('end') - x0
    yw = plot.y_range.__getattribute__('end') - y0
    max_iterations = int(max_iter.value)
    frequency = int(np.mean(iterations[iterations!=max_iterations])/new*10)

    print "calculating colors."
    col = mandel_colormap.it_count_to_color(iterations, frequency, max_iterations)
    img = mandel_colormap.rgb_color_to_bokeh_rgba(color=col)
    print "done."

    print "updating data."
    source_image.data = dict(image=[img], x0=[x0], y0=[y0], xw=[xw], yw=[yw], max_iter=[max_iterations], freq=[new])
    print "data was updated."


def update_data():
    x0 = plot.x_range.__getattribute__('start')
    y0 = plot.y_range.__getattribute__('start')
    xw = plot.x_range.__getattribute__('end')-x0
    yw = plot.y_range.__getattribute__('end')-y0
    max_iterations = int(max_iter.value)

    change_param = False
    change_param = change_param or (source_image.data['x0'][0] != x0)
    change_param = change_param or (source_image.data['y0'][0] != y0)
    change_param = change_param or (source_image.data['xw'][0] != xw)
    change_param = change_param or (source_image.data['yw'][0] != yw)
    change_param = change_param or (source_image.data['max_iter'][0] != max_iterations)
    change_freq = (source_image.data['freq'][0] != freq.value)

    if change_param:
        print "change in parameters."
        print "calling mandel."
        iterations = mandel.mandel(x0, y0, xw, yw, 400, 400, max_iterations, 10)
        print "done."
        print "updating data."
        source_its.data = dict(its=[iterations])
        print "done."
    else:
        print "no change in parameters, data update skipped"

    if change_freq or change_param:
        print "change in color."
        print "calling update_image"
        update_image(None,None,freq.value)
    else:
        print "no change in color, color update skipped"


# initialize data
update_data()

# setup callback
freq.on_change('value',update_image)

# update picture all 100 ms w.r.t current view
curdoc().add_periodic_callback(update_data, 100)
# make layout
curdoc().add_root(VBox(children=[plot, max_iter, freq]))

print "everything initialized."
