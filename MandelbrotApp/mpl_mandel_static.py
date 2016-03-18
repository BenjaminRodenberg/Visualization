from __future__ import division

import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np

import mandel_par
from scipy.ndimage.filters import gaussian_filter, median_filter
from scipy.interpolate import PchipInterpolator
import scipy.misc as smp

def get_color_interpolator():
    '''
    Monotone cubic spline interpolation is used
    '''

    x = [0.0, 0.16, 0.42, 0.6425, 0.8575,1.0]
    c = [(0,   7,   100),
         (32,  107, 203),
         (237, 255, 255),
         (255, 170, 0),
         (0,   2,   0),
         (0,   7,   100)]
    # alternative colormap
    '''
    c = [(66, 30, 15),  # brown 3
         (25, 7, 26),  # dark violett
         (9, 1, 47),  # darkest blue
         (4, 4, 73),  # blue 5
         (0, 7, 100),  # blue 4
         (12, 44, 138),  # blue 3
         (24, 82, 177),  # blue 2
         (57, 125, 209),  # blue 1
         (134, 181, 229),  # blue 0
         (211, 236, 248),  # lightest blue
         (241, 233, 191),  # lightest yellow
         (248, 201, 95),  # light yellow
         (255, 170, 0),  # dirty yellow
         (204, 128, 0),  # brown 0
         (153, 87, 0),  # brown 1
         (106, 52, 3),  # brown 2
         (66, 30, 15)]  # brown 3 again
    x = np.linspace(0,1,c.__len__()).tolist()
    '''
    r = [c[i][0] for i in range(c.__len__())]
    g = [c[i][1] for i in range(c.__len__())]
    b = [c[i][2] for i in range(c.__len__())]

    r_interp = PchipInterpolator(x,r)
    g_interp = PchipInterpolator(x,g)
    b_interp = PchipInterpolator(x,b)

    '''
    c_interp = lambda x: np.array((r_interp(x%1)+r_interp((x+1/16)%1),
                                   g_interp(x%1)+g_interp((x+1/16)%1),
                                   b_interp(x%1)+b_interp((x+1/16)%1))).transpose()
    '''
    c_interp = lambda x: np.array((r_interp(x),g_interp(x),b_interp(x))).transpose()

    return c_interp,c

x_res = 2000
y_res = 2000


# Spiral
name = 'mandel_spiral.png'
cx = -0.74364085
cy = 0.13182733
d = 0.000120168
n_sample = 32
iterations = 10000
iteration_bound = 10
median_filtering_size = 0
gauss_filtering_sigma = 0
shift = 3


#Lightning
name = 'mandel_lightning.png'
cx = 0.37144264
cy = 0.64935303
d = 0.00005
n_sample = 256
iterations = 10000
iteration_bound = 10
shift = 0
median_filtering_size = 0
gauss_filtering_sigma = 0


#Tail
name = 'mandel_tail.png'
cx = -0.7435669
cy = 0.1314023
d = 0.0022878
n_sample = 64
iterations = 10*n_sample
iteration_bound = 10
median_filtering_size = x_res / 100
gauss_filtering_sigma = 1


#ganz
name = 'mandel_ganz.png'
cx = -0.5
cy = 0
d = 3
n_sample = 16
iterations = 10000
iteration_bound = 10
median_filtering_size = 0
gauss_filtering_sigma = 0
shift = -2

x0 = cx-d*.5
y0 = cy-d*.5
xw = d
yw = d

re,im,z,re_z,im_z = mandel_par.mandel(x0, y0, xw, yw, x_res, y_res, iterations,iteration_bound)
if median_filtering_size is not 0:
    z = median_filter(z, size=median_filtering_size)

if gauss_filtering_sigma is not 0:
    z = gaussian_filter(z,sigma=gauss_filtering_sigma)



c_interp,c_pal = get_color_interpolator()

#z=z+shift
z[z==iterations]=-1
color = c_interp((z%n_sample)/n_sample).transpose()
color[0,z==-1]=0.0
color[1,z==-1]=0.0
color[2,z==-1]=0.0

img = smp.toimage(color) # Create a PIL image
img.save(name)
img.show()


