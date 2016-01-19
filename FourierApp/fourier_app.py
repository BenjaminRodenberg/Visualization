import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import VBox, Slider, RadioButtonGroup, VBoxForm, Dropdown, TextInput
from bokeh.models import Plot, ColumnDataSource
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
fourier_settings = import_bokeh('fourier_settings.py')

# initialize data source
source_fourier = ColumnDataSource(data=dict(t=[], x_fourier=[]))
source_orig = ColumnDataSource(data=dict(t=[], x_orig=[]))


def update_data():
    # ==============================================================================
    #         Called each time that any watched property changes.
    #
    #         This updates the fourier series expansion with the most recent values
    #         of the slider. The new fourier series y data is stored as a numpy
    #         arrays in a dict into the app's data source property.
    # ==============================================================================
    N = int(round(degree.value))  # Get the current slider values
    f_raw = fourier_settings.function_library[function_type.active]

    # function f(x) which will be approximated
    t = np.linspace(fourier_settings.x_min, fourier_settings.x_max, fourier_settings.resolution)
    x_orig = np.empty(len(t))

    if function_type.active == 3:
        fun_str = function_input.value
        f = f_raw(fun_str)
    else:
        function_input.value = fourier_settings.function_input_msg
        f = f_raw

    for i in range(len(t)):
        periodic_t = (t[i] - fourier_settings.timeinterval_start) \
                     % fourier_settings.timeinterval_length + \
                     fourier_settings.timeinterval_start
        x_orig[i] = f(periodic_t)

    # Generate Fourier series
    T = fourier_settings.timeinterval_length  # length of one period of the function
    a, b = ff.coeff(f, fourier_settings.timeinterval_start, fourier_settings.timeinterval_end,
                    N)  # calculate coefficients
    x_fourier = np.empty(len(x_orig))

    for i in range(len(x_fourier)):  # evaluate fourier series
        x_fourier[i] = ff.fourier_series(a, b, T, t[i])

    # saving data to plot
    source_orig.data = dict(t=t, x_orig=x_orig)
    source_fourier.data = dict(t=t, x_fourier=x_fourier)

    # generate new TeX string
    TeX_string = ft.generate_tex(a, b, T)

    print "data was updated with N = %d" % (N)

    return TeX_string


def send_request(TeX_string):
    print "sending request..."
    # urllib.urlopen("http://localhost:5001/publish?TEX="+TeX_string)


def type_input_change(attrname, old, new):
    if function_type.active == 3:
        function_input.value = fourier_settings.function_input_init
    else:
        function_input.value = fourier_settings.function_input_msg
        input_change(attrname, old, new)


def input_change(attrname, old, new):
    TeX_string = update_data()  # update data and get new TeX
    send_request(TeX_string)  # send new TeX to server


# initialize controls
# slider controlling the base function
function_type = RadioButtonGroup(labels=fourier_settings.function_names, active=fourier_settings.function_init)
# here one can choose arbitrary input function
function_input = TextInput(value=fourier_settings.function_input_msg, title="my function:")
# slider controlling degree of the fourier series
degree = Slider(title="degree", name='degree', value=fourier_settings.degree_init, start=fourier_settings.degree_min,
                end=fourier_settings.degree_max, step=fourier_settings.degree_step)

# initialize callback behaviour
degree.on_change('value', input_change)
function_input.on_change('value', input_change)
function_type.on_change('active', type_input_change)  # initialize plot
toolset = "crosshair,pan,reset,resize,save,wheel_zoom"

# Generate a figure container
plot = Figure(title_text_font_size="12pt",
              plot_height=400,
              plot_width=400,
              tools=toolset,
              title="Fourier Series Approximation",
              x_range=[fourier_settings.x_min, fourier_settings.x_max],
              y_range=[fourier_settings.y_min, fourier_settings.y_max]
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
plot.patch([fourier_settings.timeinterval_start, fourier_settings.timeinterval_start,
            fourier_settings.timeinterval_end, fourier_settings.timeinterval_end],
           [-10 ** 10, +10 ** 10, +10 ** 10, -10 ** 10],
           alpha=.2
           )
plot.line([fourier_settings.timeinterval_start, fourier_settings.timeinterval_start], [-10 ** 10, 10 ** 10])
plot.line([fourier_settings.timeinterval_end, fourier_settings.timeinterval_end], [-10 ** 10, 10 ** 10])

# calculate data
update_data()

# lists all the controls in our app
controls = VBoxForm(
        children=[
            degree,
            function_type,
            function_input
        ]
)

# make layout
curdoc().add_root(VBox(children=[plot, controls]))
