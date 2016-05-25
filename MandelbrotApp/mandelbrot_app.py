from __future__ import division

import logging
import numpy as np

from bokeh.models.widgets import VBox, Slider
from bokeh.models import ColumnDataSource, PrintfTickFormatter
from bokeh.plotting import Figure
from bokeh.io import curdoc

# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
mandel = import_bokeh('mandel.py')
mandel_colormap = import_bokeh('mandel_colormap.py')
mandelbrot_settings = import_bokeh('mandelbrot_settings.py')
my_bokeh_utils = import_bokeh('../my_bokeh_utils.py')

logging.basicConfig(level=logging.DEBUG)

# data source saving raw data (number of iterations) of mandelbrot set
source_mandel_raw = ColumnDataSource(
    data=dict(iterations=[],  # number of iterations for each point in the mandelbrot set
              max_iter=[mandelbrot_settings.iter_init]  # maximum iterations for computing the mandelbrot set
              ))

# initialize controls
# slider for maximum number of iterations for the computation of the mandelbrot set
slider_max_iterations = Slider(title="iterations",
                               name='iterations',
                               value=mandelbrot_settings.iter_init,
                               start=0,
                               end=mandelbrot_settings.iter_max,
                               step=mandelbrot_settings.iter_step)

# slider controlling the frequency of the colormap
slider_frequency = Slider(title="coloring",
                          name='coloring',
                          value=mandelbrot_settings.freq_init,
                          start=mandelbrot_settings.freq_min,
                          end=mandelbrot_settings.freq_max,
                          step=mandelbrot_settings.freq_step)

# Generate a figure container
toolset = "pan,reset,wheel_zoom,save"
plot = Figure(title_text_font_size="12pt",
              plot_height=mandelbrot_settings.x_res,
              plot_width=mandelbrot_settings.y_res,
              x_range=[mandelbrot_settings.x0, mandelbrot_settings.x0 + mandelbrot_settings.xw],
              y_range=[mandelbrot_settings.y0, mandelbrot_settings.y0 + mandelbrot_settings.yw],
              tools=toolset,
              title="Mandelbrot Set"
              )

# Plot the mandelbrot set as a image
# data source for image data
source_image = ColumnDataSource(data=dict(image=[],  # image data
                                          x0=[mandelbrot_settings.x0],  # image origin x
                                          y0=[mandelbrot_settings.y0],  # image origin y
                                          xw=[mandelbrot_settings.xw],  # image width
                                          yw=[mandelbrot_settings.yw],  # image height
                                          freq=[mandelbrot_settings.freq_init]  # frequency of the colormap
                                          ))

plot.image_rgba(image='image',  # image data from data source
                x='x0',  # image origin x
                y='y0',  # image origin y
                dw='xw',  # image width
                dh='yw',  # image height
                source=source_image)  # corresponding data source

# Turn off tick labels
plot.axis.formatter = PrintfTickFormatter(format=" ")  # create formatter
plot.axis.major_tick_line_color = None  # turn off major ticks
plot.axis.minor_tick_line_color = None  # turn off minor ticks


def update_colormap(attrname, old, new_frequency):
    """
    updates the coloring of the plot.
    :param attrname: unused, but needed for bokeh callback functions
    :param old: unused, but needed for bokeh callback functions
    :param new_frequency: new value for the frequency
    """
    x0, y0, xw, yw = my_bokeh_utils.get_user_view(plot)
    mandel_iterations = source_mandel_raw.data['its'][0]

    frequency = int(
        np.mean(mandel_iterations[mandel_iterations != int(slider_max_iterations.value)]) / new_frequency * 10)  # todo magic number?

    print "calculating colors."
    col = mandel_colormap.iteration_count_to_rgb_color(mandel_iterations, frequency, int(slider_max_iterations.value))
    img = mandel_colormap.rgb_color_to_bokeh_rgba(color=col)
    print "done."

    print "updating image data."
    source_image.data = dict(image=[img], x0=[x0], y0=[y0], xw=[xw], yw=[yw], freq=[new_frequency])
    print "data was updated."


def update_mandelbrot_set():
    """
    updates the raw data of the mandelbrot set corresponding to the current user input. Therefore the currently observed
    part of the mandelbrot set is computed using the given maximum iteration number. The output data is written to the
    corresponding bokeh.models.ColumnDataSource
    """
    x0, y0, xw, yw = my_bokeh_utils.get_user_view(plot)

    print "calculating mandelbrot set."
    mandel_iterations = mandel.mandel(x0, y0, xw, yw,  # user view
                                      mandelbrot_settings.x_res, mandelbrot_settings.y_res,  # resolution
                                      slider_max_iterations.value,  # maximum number of iterations
                                      mandelbrot_settings.iteration_bound)
    print "done."

    print "updating raw data."
    source_mandel_raw.data = dict(its=[mandel_iterations], max_iter=[int(slider_max_iterations.value)])
    print "data was updated."


def check_parameters(x0, y0, xw, yw, max_iterations):
    """
    checks for a change in the user input parameters that affect the computation of the mandelbrot set
    :param x0: origin x of the plot
    :param y0: origin y of the plot
    :param xw: width of the plot
    :param yw: height of the plot
    :param max_iterations: maximum iteration number
    :return: bool that states if any relevant parameter has been changed
    """
    parameters_have_changed = (source_image.data['x0'][0] != x0) or \
                              (source_image.data['y0'][0] != y0) or \
                              (source_image.data['xw'][0] != xw) or \
                              (source_image.data['yw'][0] != yw) or \
                              (source_mandel_raw.data['max_iter'][0] != max_iterations)
    return parameters_have_changed


def check_frequency(frequency):
    """
    checks for a change in the user input parameters that affect the computation of the colormap
    :param frequency: frequency of the colormap
    :return: bool that states if any relevant parameter has been changed
    """
    frequency_has_changed = (source_image.data['freq'][0] != frequency)
    return frequency_has_changed


def update_data():
    """
    function that checks for changes in the user input and if changes are observed, the corresponding data is updated.
    The two main tasks of this function are:
        1.  if any relevant parameters for the computation of the mandelbrot set have changed, recompute mandelbrot set
            and update the image data as well as the coloring of the image.
        2.  if any relevant parameters for the computation of the colormap have changed, apply the colormap to unchanged
            raw mandelbrot set data and save the changed colors to the corresponding data source
    """
    x0, y0, xw, yw = my_bokeh_utils.get_user_view(plot)

    parameters_have_changed = check_parameters(x0, y0, xw, yw, slider_max_iterations.value)
    frequency_has_changed = check_frequency(slider_frequency.value)

    if parameters_have_changed:
        update_mandelbrot_set()
        update_colormap(None, None, slider_frequency.value)
        return
    elif frequency_has_changed:
        update_colormap(None, None, slider_frequency.value)
        return
    else:
        return


# initialize data
update_mandelbrot_set()
update_colormap(None, None, slider_frequency.value)

# setup callback for colormap frequency change
slider_frequency.on_change('value', update_colormap)

# update picture all 100 ms w.r.t current view
curdoc().add_periodic_callback(update_data, mandelbrot_settings.update_time)
# make layout
curdoc().add_root(VBox(children=[plot, slider_max_iterations, slider_frequency]))