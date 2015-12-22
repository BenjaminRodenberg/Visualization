__author__ = 'benjamin'


def quiver(self, **kwargs):
    import numpy as np

    print "QUIVER EVAL!"

    def __t_matrix(translate_x,translate_y):
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

            x1 = x0+u
            x_patch[0] = x1
            x_patch[1] = x1-headsize
            x_patch[2] = x1-headsize

            y1 = y0+v
            y_patch[0] = y1
            y_patch[1] = y1+headsize/np.sqrt(3)
            y_patch[2] = y1-headsize/np.sqrt(3)
        elif type_id is 1:
            x_patch = 4 * [None]
            y_patch = 4 * [None]

            x1 = x0+u
            x_patch[0] = x1
            x_patch[1] = x1-headsize
            x_patch[2] = x1-headsize/2
            x_patch[3] = x1-headsize

            y1 = y0+v
            y_patch[0] = y1
            y_patch[1] = y1+headsize/np.sqrt(3)
            y_patch[2] = y1
            y_patch[3] = y1-headsize/np.sqrt(3)
        else:
            raise Exception("unknown head type!")

        return x_patch, y_patch

    def __get_patch_data(x0, y0, u, v, headsize):

        angle = np.arctan(v/u)

        x_patch, y_patch = __head_template(x0, y0, u, v, type_id=1, headsize=headsize)

        T1 = __t_matrix(-x_patch[0], -y_patch[0])
        R = __r_matrix(angle)
        T2 = __t_matrix(x_patch[0], y_patch[0])
        T = T2.dot(R.dot(T1))

        for i in range(x_patch.__len__()):
            v_in = np.array([x_patch[i],y_patch[i],1])
            v_out = T.dot(v_in)
            x_patch[i], y_patch[i], tmp = v_out

        return x_patch, y_patch

    def __plot_arrowheads(self, X, Y, U, V, size):
        n_arrows = X.shape[0]
        x_patches = n_arrows * [None]
        y_patches = n_arrows * [None]

        for i in range(n_arrows):
            x_patch, y_patch = __get_patch_data(X[i],Y[i],U[i],V[i],size)
            x_patches[i] = x_patch
            y_patches[i] = y_patch

        self.patches(xs=x_patches,ys=y_patches)

    try:
        x = kwargs.pop('x')
        y = kwargs.pop('y')
        u = kwargs.pop('u')
        v = kwargs.pop('v')
        h = kwargs.pop('h')
    except:
        raise Exception('Not enough values given! Quiver needs at least x, y, u, v, h.')

    if 'source' in kwargs:
        source = kwargs.pop('source')
        x = source.data[x]
        y = source.data[y]
        u = source.data[u]
        v = source.data[v]
        h = source.data[h]

    x = x.flatten()
    y = y.flatten()
    u = u.flatten()
    v = v.flatten()

    length = np.sqrt(u**2+v**2)
    u = u / length * h *.9
    v = v / length * h *.9
    self.segment(x0=x, y0=y, x1=x+u, y1=y+v)
    __plot_arrowheads(self, x, y, u, v, h/4)

import bokeh
bokeh.plotting.Figure.quiver = quiver
