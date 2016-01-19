from __future__ import division

import logging

from bokeh.models.widgets import VBox, Button, TextInput
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
mandel_par = import_bokeh('mandel_par.py')

logging.basicConfig(level=logging.DEBUG)

# initialize data source
source_image = ColumnDataSource(data=dict(image=[], x0=[], y0=[], xw=[], yw=[]))
source_fig_specs = ColumnDataSource(data=dict(x0=[], y0=[], xw=[], yw=[]))

# initialize controls
refresh = Button(label="Refresh plot")
max_iter = TextInput(title="iterations", value='50')

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
plot.image(image='image',
           x='x0',
           y='y0',
           dw='xw',
           dh='yw',
           palette="Spectral11",
           source=source_image)


def update_data():
    x0 = plot.x_range.__getattribute__('start')
    y0 = plot.y_range.__getattribute__('start')
    xw = plot.x_range.__getattribute__('end')-x0
    yw = plot.y_range.__getattribute__('end')-y0

    iterations = int(max_iter.value)

    print "calling mandel."
    z = mandel_par.mandel(x0, y0, xw, yw, 400, 400, iterations)
    print "done."

    source_image.data = dict(image=[z.tolist()], x0=[x0], y0=[y0], xw=[xw], yw=[yw])

    print "data was updated."
    param = dict(x0=x0, y0=y0, xw=xw, yw=yw)
    print param


def refresh_plot():
    print "REFRESH!"
    update_data()


# initialize data
update_data()

# setup callback
refresh.on_click(refresh_plot)

# make layout
curdoc().add_root(VBox(children=[plot, max_iter, refresh]))

print "everything initialized."
