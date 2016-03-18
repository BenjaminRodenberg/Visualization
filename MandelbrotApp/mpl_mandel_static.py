from __future__ import division

import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np

import mandel
from scipy.ndimage.filters import gaussian_filter, median_filter
from scipy.interpolate import PchipInterpolator
import scipy.misc as smp

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

# target resolution
x_res = 200
y_res = 200


# in the following you find some sample setups.

# Spiral
name = 'mandel_spiral.png'
cx = -0.74364085
cy = 0.13182733
d = 0.000120168
frequency = 32
iterations = 10000
iteration_bound = 10
median_filtering_size = 0
gauss_filtering_sigma = 0

#Lightning
name = 'mandel_lightning.png'
cx = 0.37144264
cy = 0.64935303
d = 0.00005
frequency = 256
iterations = 10000
iteration_bound = 10
median_filtering_size = 0
gauss_filtering_sigma = 0

#Tail
name = 'mandel_tail.png'
cx = -0.7435669
cy = 0.1314023
d = 0.0022878
frequency = 64
iterations = 10 * frequency
iteration_bound = 10
median_filtering_size = x_res / 100
gauss_filtering_sigma = 1

#ganz
name = 'mandel_ganz.png'
cx = -0.5
cy = 0
d = 3
frequency = 16
iterations = 10000
iteration_bound = 100
median_filtering_size = 0
gauss_filtering_sigma = 0.1

x0 = cx-d*.5
y0 = cy-d*.5
xw = d
yw = d

### main process starts here. ###

# calculate mandelbrot set
it_count = mandel.mandel(x0, y0, xw, yw, x_res, y_res, iterations, iteration_bound)

# apply some filters
if median_filtering_size is not 0:
    it_count = median_filter(it_count, size=median_filtering_size)
if gauss_filtering_sigma is not 0:
    it_count = gaussian_filter(it_count, sigma=gauss_filtering_sigma)

# get colormap
c_interp = get_color_interpolator()
# color set according to colormap (coloring a cyclic fashion with a predefined fequency)
color = c_interp((it_count % frequency) / frequency).transpose()
# explicitly color regions, where maximum iteration was reached, black
color[0, it_count == iterations]=0.0  # red channel = 0
color[1, it_count == iterations]=0.0  # blue channel = 0
color[2, it_count == iterations]=0.0  # green channel = 0

# plot and save picture
img = smp.toimage(color) # Create a PIL image
img.save(name)
img.show()


