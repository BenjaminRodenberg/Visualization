from __future__ import division
import numpy as np
import time


def mandel(x0,y0,xw,yw,x_res,y_res, iterate_max):
    # Calculate the mandelbrot sequence for the point c with start value z
    def iterate_mandelbrot(c_re, c_im):
        re = 0
        im = 0
        for n in xrange(iterate_max + 1):
            xx = re * re
            yy = im * im
            xy = re * im
            re = xx - yy + c_re
            im = 2 * xy + c_im
            if (xx+yy) > 2:
                return n/iterate_max
        return 1.0

    t0 = time.clock()

    # Draw our image
    x, y = np.meshgrid(np.linspace(x0,x0+xw,x_res), np.linspace(y0,y0+yw,y_res))
    z = np.zeros(x.shape)
    for i in xrange(x.shape[0]):
        for j in xrange(y.shape[1]):
            re = x[i,j]
            im = y[i,j]
            z[i,j] = iterate_mandelbrot(re, im)

    print "elapsed time:"+str(time.clock()-t0)+" sec"

    return z


