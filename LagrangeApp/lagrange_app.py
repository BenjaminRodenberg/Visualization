"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""
# ==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
# ==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import Slider, HBox, TextInput, Panel, Tabs, Dropdown, VBoxForm, VBox
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure
from bokeh.io import curdoc

import numpy as np

# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
my_bokeh_utils = import_bokeh('../my_bokeh_utils.py')
lagrange_settings = import_bokeh('lagrange_settings.py')

# initialize data source
source_contour = ColumnDataSource(data=dict(xs=[], ys=[], line_colors=[]))  # multilines drawing a contour plot
source_isolevel = ColumnDataSource(data=dict(xs=[], ys=[], line_colors=[]))  # multilines drawing a contour plot
source_isolevel_grad = ColumnDataSource(data=dict(x=[], y=[], x0=[], y0=[], x1=[], y1=[], xs=[], ys=[]))
source_constraint = ColumnDataSource(data=dict(xs=[], ys=[], line_colors=[]))  # multilines drawing isocontour g(x,y)=0
source_constraint_grad = ColumnDataSource(data=dict(x=[], y=[], x0=[], y0=[], x1=[], y1=[], xs=[], ys=[]))
source_mark = ColumnDataSource(data=dict(x=[],y=[]))
source_view = ColumnDataSource(data=dict(x_start=[lagrange_settings.x_min],
                                         x_end=[lagrange_settings.x_max],
                                         y_start=[lagrange_settings.y_min],
                                         y_end=[lagrange_settings.y_max]))  # user view information


def init_data():
    f, _ = my_bokeh_utils.string_to_function_parser(f_input.value,['x','y'])
    source_contour.data = compute_contour_data(f)
    g, _ = my_bokeh_utils.string_to_function_parser(g_input.value,['x','y'])
    source_constraint.data = compute_contour_data(g, [0])
    interactor.update_to_user_view()


def compute_contour_data(f, isovalue=None):
    x, y = np.meshgrid(np.linspace(plot.x_range.start, plot.x_range.end, lagrange_settings.res_x),
                       np.linspace(plot.y_range.start, plot.y_range.end, lagrange_settings.res_y))

    z = f(x, y)

    source = my_bokeh_utils.get_contour_data(x, y, z, isovalue=isovalue)

    return source.data


def compute_gradient_data(df, x0, y0):
    dfx_val, dfy_val = df(x0,y0)
    ssdict, spdict, _ = my_bokeh_utils.quiver_to_data(x=np.array(x0),
                                                      y=np.array(y0),
                                                      u=np.array(dfx_val),
                                                      v=np.array(dfy_val),
                                                      h=(source_view.data['x_end'][0] - source_view.data['x_start'][0] ) / 10.0,
                                                      do_normalization=True,
                                                      fix_at_middle=False)

    return dict(x=[x0], y=[y0],
                x0=ssdict['x0'], y0=ssdict['y0'],
                x1=ssdict['x1'], y1=ssdict['y1'],
                xs=spdict['xs'], ys=spdict['ys'])


# initialize plot
toolset = ["crosshair,pan,reset,resize,save,wheel_zoom,tap"]
# Generate a figure container for the field
plot = Figure(title_text_font_size="12pt",
              plot_height=lagrange_settings.res_x,
              plot_width=lagrange_settings.res_y,
              tools=toolset,
              title="Vector valued function",
              x_range=[lagrange_settings.x_min, lagrange_settings.x_max],
              y_range=[lagrange_settings.y_min, lagrange_settings.y_max]
              )

plot.multi_line(xs='xs', ys='ys', line_color='gray', line_width=1, source=source_contour)
# Plot active isolevel
plot.multi_line(xs='xs', ys='ys', line_color='black', line_width=2, source=source_isolevel, legend='f(x,y) = v')
# Plot corresponding tangent vector
plot.segment('x0', 'y0', 'x1', 'y1', source=source_isolevel_grad, color='black')
plot.patches('xs', 'ys', source=source_isolevel_grad, color='black')
# Plot corresponding isovalue label
plot.text(x='xt', y='yt', text='text', source=source_isolevel, text_baseline='middle', text_align='center')
# Plot constraint function contour
plot.multi_line(xs='xs', ys='ys', line_color='red', line_width=2, source=source_constraint, legend='g(x,y) = 0')
# Plot corresponding tangent vector
plot.segment('x0', 'y0', 'x1', 'y1', source=source_constraint_grad, color='red')
plot.patches('xs', 'ys', source=source_constraint_grad, color='red')
# Plot mark at position on constraint function
plot.cross(x='x',y='y', color='red', size=10, line_width=2, source=source_mark)


def on_selection_change(attr, old, new):
    x_coor, y_coor = interactor.clicked_point(new)

    # todo save original and gradient functions to data source!
    f, f_sym = my_bokeh_utils.string_to_function_parser(f_input.value,['x','y'])
    g, g_sym = my_bokeh_utils.string_to_function_parser(g_input.value,['x','y'])

    # calculate gradient function
    from sympy import diff
    dg_list = []
    df_list = []
    for s in ['x','y']:
        dgds_sym = diff(g_sym,s)
        dfds_sym = diff(f_sym,s)
        dg_list.append(my_bokeh_utils.sym_to_function_parser(dgds_sym,['x','y']))
        df_list.append(my_bokeh_utils.sym_to_function_parser(dfds_sym,['x','y']))
    dg = lambda x, y: [_(x, y) for _ in dg_list]
    df = lambda x, y: [_(x, y) for _ in df_list]

    # detect clicked point
    print "clicked point: (%f,%f)" %(x_coor,y_coor)
    x_close, y_close = my_bokeh_utils.find_closest_on_iso(x_coor,y_coor,g)
    print "closest point on g: (%f,%f)" % (x_close, y_close)
    isovalue = f(x_close, y_close)
    print isovalue
    source_isolevel.data = compute_contour_data(f, [isovalue])
    source_isolevel_grad.data = compute_gradient_data(df, x_close, y_close)
    source_constraint_grad.data = compute_gradient_data(dg, x_close, y_close)

    source_mark.data = dict(x=[x_close],y=[y_close])


def on_function_change(attr, old, new):
    # todo save original and gradient functions to data source!
    f, f_sym = my_bokeh_utils.string_to_function_parser(f_input.value, ['x', 'y'])
    g, g_sym = my_bokeh_utils.string_to_function_parser(g_input.value, ['x', 'y'])

    x_mark = source_mark.data['x']
    y_mark = source_mark.data['y']
    if len(x_mark) > 0:
        isovalue = f(x_mark[0], y_mark[0])
        source_isolevel.data = compute_contour_data(f, [isovalue])

        from sympy import diff
        dg_list = []
        df_list = []
        for s in ['x', 'y']:
            dgds_sym = diff(g_sym, s)
            dfds_sym = diff(f_sym, s)
            dg_list.append(my_bokeh_utils.sym_to_function_parser(dgds_sym, ['x', 'y']))
            df_list.append(my_bokeh_utils.sym_to_function_parser(dfds_sym, ['x', 'y']))
        dg = lambda x, y: [_(x, y) for _ in dg_list]
        df = lambda x, y: [_(x, y) for _ in df_list]
        source_isolevel_grad.data = compute_gradient_data(df, x_mark[0], y_mark[0])
        source_constraint_grad.data = compute_gradient_data(dg, x_mark[0], y_mark[0])

    source_contour.data = compute_contour_data(f)
    source_constraint.data = compute_contour_data(g, [0])
    source_view.data = my_bokeh_utils.get_user_view(plot)


def refresh_contour():
    """
    periodically called function that updates data with respect to the current user view, if the user view has changed.
    :return:
    """
    user_view_has_changed = my_bokeh_utils.check_user_view(source_view.data, plot)
    if user_view_has_changed:
        f, _ = my_bokeh_utils.string_to_function_parser(f_input.value,['x','y'])
        g, _ = my_bokeh_utils.string_to_function_parser(g_input.value,['x','y'])

        x_mark = source_mark.data['x']
        y_mark = source_mark.data['y']
        if len(x_mark) > 0:
            isovalue = f(x_mark[0], y_mark[0])
            source_isolevel.data = compute_contour_data(f, [isovalue])

        source_contour.data = compute_contour_data(f)
        source_constraint.data = compute_contour_data(g, [0])
        interactor.update_to_user_view()
        source_view.data = my_bokeh_utils.get_user_view(plot)


# object that detects, if a position in the plot is clicked on
interactor = my_bokeh_utils.Interactor(plot)
# adds callback function to interactor, if position in plot is clicked, call on_selection_change
interactor.on_click(on_selection_change)

# text input window for objective function f(x,y) to be optimized
f_input = TextInput(value=lagrange_settings.f_init, title="f(x,y):")
f_input.on_change('value',on_function_change)

# text input window for side condition g(x,y)=0
g_input = TextInput(value=lagrange_settings.g_init, title="g(x,y):")
g_input.on_change('value',on_function_change)

# calculate data
init_data()

# refresh quiver field all 100ms
curdoc().add_periodic_callback(refresh_contour, 100)
# make layout
curdoc().add_root(VBoxForm(children=[HBox(children=[plot,VBox(children=[f_input,g_input])])]))
