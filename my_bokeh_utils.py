def get_user_view(plot):
    """
    returns the current user view of the plot
    :param plot: a bokeh.plotting.Figure
    :return:
    """
    x0 = plot.x_range.__getattribute__('start')  # origin x
    y0 = plot.y_range.__getattribute__('start')  # origin y
    xw = plot.x_range.__getattribute__('end') - x0  # width
    yw = plot.y_range.__getattribute__('end') - y0  # height
    return x0, y0, xw, yw