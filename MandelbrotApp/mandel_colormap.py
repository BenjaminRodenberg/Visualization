from scipy.interpolate import PchipInterpolator
import numpy as np
from numba import vectorize, guvectorize

def get_color_interpolator():
    '''
    Monotone cubic spline interpolation is used
    for color scheme see
    http://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
    '''

    # color scheme
    x = [0.0, 0.16, 0.42, 0.6425, 0.8575,1.0]
    c = [(0,   7,   100),
         (32,  107, 203),
         (237, 255, 255),
         (255, 170, 0),
         (0,   2,   0),
         (0,   7,   100)]  # added for making colors cyclic
    # extracting color channels
    r = [c[i][0] for i in range(c.__len__())]
    g = [c[i][1] for i in range(c.__len__())]
    b = [c[i][2] for i in range(c.__len__())]
    # using monotone cubic spline interpolation
    r_interp = PchipInterpolator(x,r)
    g_interp = PchipInterpolator(x,g)
    b_interp = PchipInterpolator(x,b)
    # wrapping all color channels into one function
    c_interp = lambda x: np.array((r_interp(x),g_interp(x),b_interp(x))).transpose()

    return c_interp


def rgb_color_to_bokeh_rgba(color):

    n = color.shape[1]
    m = color.shape[2]

    color = color.astype(np.uint32)

    print color[:,0,0]
    cc = np.hstack([color[:,0,0].astype(np.uint8),255])
    cc = cc.astype(np.uint32)
    print cc
    cc_img = ((cc[0] << (0 * 8)) + (cc[1] << (1 * 8)) + (cc[2] << (2 * 8)) + (255 << (3 * 8))).astype(np.uint32)
    print cc_img
    print cc.view(dtype=np.uint32)
    img = ((color[0,:,:]<<(0*8))+(color[1,:,:]<<(1*8))+(color[2,:,:]<<(2*8))+(255<<(3*8))).astype(np.uint32)
    print img.shape
    print img.dtype
    print type(img)
    '''
    color_a = np.vstack([color.astype(np.uint8), 255*np.ones([1,n,m], dtype=np.uint8)])
    color_a = np.rollaxis(color_a,0,3)
    print color_a[0:2,0:2,:].astype(np.uint8)#.view(np.uint32).shape
    img = np.array(color_a.astype(np.uint8).view(np.uint8))
    print img.shape

    img = np.empty((n, m), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((n, m, 4))
    for i in range(n):
        for j in range(m):
            view[i, j, 0] = color[0,i,j]
            view[i, j, 1] = color[1,i,j]
            view[i, j, 2] = color[2,i,j]
            view[i, j, 3] = 255
    '''
    return img

def it_count_to_color(it_count, frequency, max_iteration):
    # get colormap
    c_interp = get_color_interpolator()
    # color set according to colormap (coloring a cyclic fashion with a predefined fequency)
    color = c_interp((it_count % frequency) / frequency).transpose()
    # explicitly color regions, where maximum iteration was reached, black
    color[0, it_count == max_iteration]=0.0  # red channel = 0
    color[1, it_count == max_iteration]=0.0  # green channel = 0
    color[2, it_count == max_iteration]=0.0  # blue channel = 0

    return color
