import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import VBox, HBox, Slider, RadioButtonGroup, TextInput, Panel, Tabs, DateRangeSlider
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
ff = import_bokeh('fourier_functions.py')
ft = import_bokeh('fourier_tex.py')
fs = import_bokeh('fourier_settings.py')


def update_data():
    # ==============================================================================
    #         Called each time that any watched property changes.
    #
    #         This updates the fourier series expansion with the most recent values
    #         of the slider. The new fourier series y data is stored as a numpy
    #         arrays in a dict into the app's data source property.
    # ==============================================================================
    N = int(round(degree.value))  # Get the current slider values

    if fun_tabs.active == 0:
        f = fs.function_library[sample_function_type.active]
        timeinterval_start_str = fs.timeinterval_start_init
        timeinterval_end_str = fs.timeinterval_end_init
    elif fun_tabs.active == 1:
        fun_str = default_function_input.value
        f = ff.parser(fun_str)
        timeinterval_start_str = default_function_period_start.value
        timeinterval_end_str = default_function_period_end.value

    timeinterval_start = ff.number_parser(timeinterval_start_str)
    timeinterval_end = ff.number_parser(timeinterval_end_str)
    timeinterval_length = timeinterval_end - timeinterval_start

    # function f(x) which will be approximated
    t = np.linspace(fs.x_min, fs.x_max, fs.resolution)
    periodic_t = (t - timeinterval_start) % timeinterval_length + timeinterval_start
    x_orig = f(periodic_t)

    # Generate Fourier series
    T = timeinterval_length  # length of one period of the function
    a, b = ff.coeff(f, timeinterval_start, timeinterval_end,
                    N)  # calculate coefficients
    x_fourier = np.empty(len(x_orig))

    for i in range(len(x_fourier)):  # evaluate fourier series
        x_fourier[i] = ff.fourier_series(a, b, T, t[i])

    x_min = plot.x_range.start
    x_max = plot.x_range.end
    y_min = plot.y_range.start
    y_max = plot.y_range.end

    # saving data to plot
    source_orig.data = dict(t=t, x_orig=x_orig)
    source_fourier.data = dict(t=t, x_fourier=x_fourier)
    source_interval_patch.data = dict(x_patch=[timeinterval_start, timeinterval_end, timeinterval_end, timeinterval_start],
                                      y_patch=[y_min, y_min, y_max, y_max])
    source_interval_bound.data = dict(x_min = [timeinterval_start, timeinterval_start],
                                      x_max = [timeinterval_end, timeinterval_end],
                                      y_minmax = [y_min, y_max])
    # generate new TeX string
    TeX_string = ft.generate_tex(a, b, T)

    print "data was updated with N = %d" % (N)

    print fun_tabs.active

    return TeX_string


def send_request(TeX_string):
    print "sending request..."
    # urllib.urlopen("http://localhost:5001/publish?TEX="+TeX_string)


def type_input_change(attrname, old, new):
    input_change(attrname, old, new)


def input_change(attrname, old, new):
    TeX_string = update_data()  # update data and get new TeX
    send_request(TeX_string)  # send new TeX to server


# initialize data source
source_fourier = ColumnDataSource(data=dict(t=[], x_fourier=[]))
source_orig = ColumnDataSource(data=dict(t=[], x_orig=[]))
source_interval_patch = ColumnDataSource(data=dict(x_patch=[], y_patch=[]))
source_interval_bound = ColumnDataSource(data=dict(x_min=[],x_max=[],y_minmax=[]))

# initialize controls
# buttons for choosing a sample function
sample_function_type = RadioButtonGroup(labels=fs.function_names, active=fs.function_init)

# here one can choose arbitrary input function
default_function_input = TextInput(value=fs.function_input_init)
default_function_period_start = TextInput(title='start',value=fs.timeinterval_start_init)
default_function_period_end = TextInput(title='end',value=fs.timeinterval_end_init)

# slider controlling degree of the fourier series
degree = Slider(title="degree", name='degree', value=fs.degree_init, start=fs.degree_min,
                end=fs.degree_max, step=fs.degree_step)

# initialize callback behaviour
degree.on_change('value', input_change)
default_function_input.on_change('value', input_change)
default_function_period_start.on_change('value', input_change)
default_function_period_end.on_change('value', input_change)
sample_function_type.on_change('active', type_input_change)  # initialize plot

toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt",
              plot_height=400,
              plot_width=400,
              tools=toolset,
              title="Fourier Series Approximation",
              x_range=[fs.x_min, fs.x_max],
              y_range=[fs.y_min, fs.y_max]
              )
# Plot the line by the x,y values in the source property
plot.line('t', 'x_orig', source=source_orig,
          line_width=3,
          line_alpha=0.6,
          color='red',
          legend='original function'
          )
plot.line('t', 'x_fourier', source=source_fourier,
          color='green',
          line_width=3,
          line_alpha=0.6,
          legend='fourier series'
          )

plot.patch('x_patch', 'y_patch', source=source_interval_patch, alpha=.2)
plot.line('x_min','y_minmax', source=source_interval_bound)
plot.line('x_max','y_minmax', source=source_interval_bound)

sample_controls = VBox(width=400,
                       children=[sample_function_type])

default_controls = VBox(width=400,
                        children=[default_function_input,
                                 HBox(width=400,
                                      children=[VBox(width=20),default_function_period_start,VBox(width=10),
                                                default_function_period_end,VBox(width=20)])])

# Panels for sample functions or default functions
sample_funs = Panel(child=sample_controls, title='sample function')
default_funs = Panel(child=default_controls, title='default function')
# Add panels to tabs
fun_tabs = Tabs(tabs=[sample_funs,default_funs])

# lists all the controls in our app
controls = HBox(width=400,
                children=[VBox(),
                          VBox(children=[HBox(children=[degree],height=50),
                                         HBox(children=[fun_tabs],height=100)]),
                          VBox()])
# make layout
curdoc().add_root(VBox(children=[plot,controls],height=550,width=400))

# initialize data
update_data()
