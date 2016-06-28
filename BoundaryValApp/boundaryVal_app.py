from bokeh.models import ColumnDataSource, Button, VBox, HBox, DataTable, TableColumn
from bokeh.plotting import Figure, curdoc
from bokeh.layouts import widgetbox

import numpy as np


# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
from tables.description import Col


def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
bv_math = import_bokeh('boundaryVal_math.py')
bv_help = import_bokeh('boundaryVal_helper.py')
bv_settings = import_bokeh('boundaryVal_settings.py')


def shootChange(attrname, old, new):
    print "shootChange(...) called..."
    if buttonShortSameFar.active is 1:
        print "doing nothing!"
        print "shootChange(...) exited!"
        return
    if buttonShortSameFar.active is 0:
        print "shoot shorter!"
        shootShorter()
    elif buttonShortSameFar.active is 2:
        print "shoot further!"
        shootFurther()
    else:
        print "unknown shooting!"

    print "new alpha = %d " % app_data.data['alpha'][0]
    print "new alpha_left = %d " % app_data.data['alpha_left'][0]
    print "new alpha_right = %d " % app_data.data['alpha_right'][0]
    buttonShortSameFar.active = 1
    buttonShortSameFar.labels[1] = str(app_data.data['alpha'][0])
    print "shootChange(...) exited!"


def shootFurther():
    print "shootFurther(...) called..."
    print "old alpha = %d " % app_data.data['alpha'][0]
    print "old alpha_left = %d " % app_data.data['alpha_left'][0]
    print "old alpha_right = %d " % app_data.data['alpha_right'][0]

    alpha_right = app_data.data['alpha_right'][0]
    alpha_left = app_data.data['alpha'][0]
    app_data.data = dict(alpha=[(alpha_left + alpha_right) / 2],
                         alpha_left=[alpha_left],
                         alpha_right=[alpha_right])
    print "new alpha = " + str(app_data.data['alpha'][0]) + "."
    update_data()
    print "shootFurther(...) exited!"


def shootShorter():
    print "shootShorter(...) called..."
    print "old alpha = %d " % app_data.data['alpha'][0]
    print "old alpha_left = %d " % app_data.data['alpha_left'][0]
    print "old alpha_right = %d " % app_data.data['alpha_right'][0]
    alpha_right = app_data.data['alpha'][0]
    alpha_left = app_data.data['alpha_left'][0]
    app_data.data = dict(alpha=[(alpha_left + alpha_right) / 2],
                         alpha_left=[alpha_left],
                         alpha_right=[alpha_right])
    print "new alpha = " + str(app_data.data['alpha'][0]) + "."
    update_data()
    print "shootShorter(...) exited!"


def update_data():
    # ==============================================================================
    #         Called each time that any watched property changes.
    #         This updates the shooting curve data with the most recent values of
    #         the sliders. This is stored as two numpy arrays in a dict into the
    #         app's data source property.
    # ==============================================================================
    print "update_data(...) called..."
    # solve shooting ODE with numerical scheme
    print "computing new data..."
    _, x = bv_math.shootAlpha(app_data.data['alpha'][0])
    _, x_short = bv_math.shootAlpha(app_data.data['alpha_left'][0])
    _, x_far = bv_math.shootAlpha(app_data.data['alpha_right'][0])
    print "new data computed."

    # buttonShortSameFar.labels[1] = str(app_data.data['alpha'][0])

    datatable_data = source_datatable.data

    global target_position
    datatable_data['shot_alpha'].append(app_data.data['alpha'][0])
    datatable_data['shot_error'].append(abs(x[0,-1]-target_position))

    source_datatable.data = dict(shot_alpha=[app_data.data['alpha'][0]],#datatable_data['shot_alpha'],
                                 shot_error=[abs(x[0,-1]-target_position)])#datatable_data['shot_error'])
    print source_datatable.data

    rx = x[0, :]
    ry = x[1, :]
    rx = rx.tolist()
    ry = ry.tolist()
    rx_short = x_short[0, :]
    ry_short = x_short[1, :]
    rx_short = rx_short.tolist()
    ry_short = ry_short.tolist()
    rx_far = x_far[0, :]
    ry_far = x_far[1, :]
    rx_far = rx_far.tolist()
    ry_far = ry_far.tolist()
    # ==============================================================================
    #         This section is not working! Problem with adding line to plot!
    # ==============================================================================
    # ==============================================================================
    #         print "storing old try..."
    #         oldrx = source.data['rx'];
    #         oldry = source.data['ry'];
    #         plot.line(oldrx,oldry,color='green')
    #         print "old try stored."
    # ==============================================================================

    print "saving data..."
    source.data = dict(rx=rx, ry=ry)
    source_short.data = dict(rx_short=rx_short, ry_short=ry_short)
    source_far.data = dict(rx_far=rx_far, ry_far=ry_far)
    print "data saved."
    print "data and plot was updated with parameters: alpha=" + str(app_data.data['alpha']) + "."
    print "update_data(...) exited!"


# initialize data source
source = ColumnDataSource(data=dict(rx=[], ry=[]))
source_short = ColumnDataSource(data=dict(rx_short=[], ry_short=[]))
source_far = ColumnDataSource(data=dict(rx_far=[], ry_far=[]))
source_datatable = ColumnDataSource(data=dict(shot_alpha=[], shot_error=[]))
app_data = ColumnDataSource(data=dict(alpha=[bv_settings.alpha_init], alpha_left=[bv_settings.alpha_left],
                                      alpha_right=[bv_settings.alpha_right]))

# initialize controls
# slider controlling alpha of the the shooter
# obj.alphaSlider = Slider(title="Abschusswinkel",
#                          name='alphaSlider',
#                          value=bv_settings.alpha_init,
#                          start=bv_settings.alpha_min,
#                          end=bv_settings.alpha_max,
#                          step=bv_settings.alpha_step
#                          )
# buttons for shooting shorter or further
buttonShort = Button(label="shoot shorter")
buttonShort.on_click(shootShorter)
buttonFar = Button(label="shoot further")
buttonFar.on_click(shootFurther)
# buttonShortSameFar = RadioButtonGroup(labels=bv_settings.button_labels, active=bv_settings.button_init)
# buttonShortSameFar.on_change('active', shootChange)

# initialize plot
toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
# Generate a figure container
plot = Figure(title_text_font_size="12pt",
              plot_height=bv_settings.fig_height,
              plot_width=bv_settings.fig_width,
              tools=toolset,
              title=bv_settings.title,  # obj.text.value,
              x_range=[bv_settings.min_x, bv_settings.max_x],
              y_range=[bv_settings.min_y, bv_settings.max_y]
              )
# Plot the line by the x,y values in the source property
plot.line('rx', 'ry',
          source=source,
          line_width=3,
          line_alpha=0.6,
          color='blue',
          legend='current shot')
plot.line('rx_short', 'ry_short',
          source=source_short,
          line_width=1,
          line_alpha=.6,
          line_dash=[4, 4],
          color='green',
          legend='old next shorter shot')
plot.line('rx_far', 'ry_far',
          source=source_far,
          line_width=1,
          line_alpha=.6,
          line_dash=[4, 4],
          color='red',
          legend='old next farther sh')

# insert picture of cannon and target
global target_position
target_position = np.random.rand() * 10
bv_help.drawTargetAt(plot, target_position)
bv_help.drawCannon(plot)

# lists all the controls in our app
controls = VBox(children=[buttonShort, buttonFar])

columns = [
    TableColumn(field="shot_alpha", title="Alpha"),
    TableColumn(field="shot_error", title="Error")
]

data_table = DataTable(source=source_datatable, columns=columns, width=400)

# calculate data
update_data()

# make layout
curdoc().add_root(VBox(children=[plot, widgetbox(buttonShort, buttonFar, data_table,width=400)]))
