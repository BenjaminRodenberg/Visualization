def get_user_view(plot):
    """
    returns the current user view of the plot
    :param plot: a bokeh.plotting.Figure
    :return:
    """
    x0 = plot.x_range.start # origin x
    y0 = plot.y_range.start  # origin y
    xw = plot.x_range.end - x0  # width
    yw = plot.y_range.end - y0  # height
    return x0, y0, xw, yw