import bokeh

def check_user_view(view_data, plot):
    """
    checks for a change in the user view that affects the plotting
    :param view_data: dict containing the current view data
    :param plot: handle to the plot
    :return: bool that states if any relevant parameter has been changed
    """
    assert type(view_data) is bokeh.core.property_containers.PropertyValueDict

    user_view_has_changed = (view_data['x_start'][0] != plot.x_range.start) or \
                            (view_data['x_end'][0] != plot.x_range.end) or \
                            (view_data['y_start'][0] != plot.y_range.start) or \
                            (view_data['y_end'][0] != plot.y_range.end)

    return user_view_has_changed


def get_user_view(plot):
    """
    returns the current user view of the plot
    :param plot: a bokeh.plotting.Figure
    :return: a dict that can be used for a bokeh.models.ColumnDataSource
    """
    x_start = plot.x_range.start # origin x
    y_start = plot.y_range.start  # origin y
    x_end = plot.x_range.end  # final x
    y_end = plot.y_range.end  # final y

    return dict(x_start=[x_start],y_start=[y_start],x_end=[x_end],y_end=[y_end])


def quiver_to_data(x, y, u, v, h):
    def __normalize(u, v, h):
        length = np.sqrt(u ** 2 + v ** 2)
        u[length > 0] *= 1.0 / length[length > 0] * h * .9
        v[length > 0] *= 1.0 / length[length > 0] * h * .9
        u[length == 0] = 0
        v[length == 0] = 0
        return u, v

    def quiver_to_segments(x, y, u, v, h):
        x = x.flatten()
        y = y.flatten()
        u = u.flatten()
        v = v.flatten()

        u, v = __normalize(u, v, h)

        x0 = x - u * .5
        y0 = y - v * .5
        x1 = x + u * .5
        y1 = y + v * .5

        return x0, y0, x1, y1

    def quiver_to_arrowheads(x, y, u, v, h):

        def __t_matrix(translate_x, translate_y):
            return np.array([[1, 0, translate_x],
                             [0, 1, translate_y],
                             [0, 0, 1]])

        def __r_matrix(rotation_angle):
            c = np.cos(rotation_angle)
            s = np.sin(rotation_angle)
            return np.array([[c, -s, 0],
                             [s, +c, 0],
                             [0, +0, 1]])

        def __head_template(x0, y0, u, v, type_id, headsize):
            if type_id is 0:
                x_patch = 3 * [None]
                y_patch = 3 * [None]

                x1 = x0 + u
                x_patch[0] = x1
                x_patch[1] = x1 - headsize
                x_patch[2] = x1 - headsize

                y1 = y0 + v
                y_patch[0] = y1
                y_patch[1] = y1 + headsize / np.sqrt(3)
                y_patch[2] = y1 - headsize / np.sqrt(3)
            elif type_id is 1:
                x_patch = 4 * [None]
                y_patch = 4 * [None]

                x1 = x0 + u
                x_patch[0] = x1
                x_patch[1] = x1 - headsize
                x_patch[2] = x1 - headsize / 2
                x_patch[3] = x1 - headsize

                y1 = y0 + v
                y_patch[0] = y1
                y_patch[1] = y1 + headsize / np.sqrt(3)
                y_patch[2] = y1
                y_patch[3] = y1 - headsize / np.sqrt(3)
            else:
                raise Exception("unknown head type!")

            return x_patch, y_patch

        def __get_patch_data(x0, y0, u, v, headsize):

            def angle_from_xy(x, y):
                if x == 0:
                    return np.pi * .5 + int(y <= 0) * np.pi
                else:
                    if y >= 0:
                        if x > 0:
                            return np.arctan(y / x)
                        elif x < 0:
                            return -np.arctan(y / -x) + np.pi
                        else:
                            return 1.5 * np.pi
                    else:
                        if x > 0:
                            return -np.arctan(-y / x)
                        elif x < 0:
                            return np.arctan(-y / -x) + np.pi
                        else:
                            return .5 * np.pi

            angle = angle_from_xy(u, v)

            x_patch, y_patch = __head_template(x0, y0, u, v, type_id=0, headsize=headsize)

            T1 = __t_matrix(-x_patch[0], -y_patch[0])
            R = __r_matrix(angle)
            T2 = __t_matrix(x_patch[0], y_patch[0])
            T = T2.dot(R.dot(T1))

            for i in range(x_patch.__len__()):
                v_in = np.array([x_patch[i], y_patch[i], 1])
                v_out = T.dot(v_in)
                x_patch[i], y_patch[i], tmp = v_out

            return x_patch, y_patch

        x = x.flatten()
        y = y.flatten()
        u = u.flatten()
        v = v.flatten()

        u, v = __normalize(u, v, h)

        n_arrows = x.shape[0]
        xs = n_arrows * [None]
        ys = n_arrows * [None]

        headsize = .1 * h

        for i in range(n_arrows):
            x_patch, y_patch = __get_patch_data(x[i] - .5 * u[i], y[i] - .5 * v[i], u[i], v[i], headsize)
            xs[i] = x_patch
            ys[i] = y_patch

        return xs, ys

    x0, y0, x1, y1 = quiver_to_segments(x, y, u, v, h)
    ssdict = dict(x0=x0, y0=y0, x1=x1, y1=y1)

    xs, ys = quiver_to_arrowheads(x, y, u, v, h)
    spdict = dict(xs=xs, ys=ys)
    sbdict = dict(x=x.flatten(), y=y.flatten())

    return ssdict, spdict, sbdict