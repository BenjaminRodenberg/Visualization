from __future__ import division
import numpy as np
from numba import vectorize, guvectorize
import time


def mandel(x0,y0,xw,yw,x_res,y_res, iterate_max, iteration_bound):
    # Calculate the mandelbrot sequence for the point c with start value z
    @guvectorize(['void(float64[:,:], float64[:,:],float64[:,:])'],'(m,n),(m,n)->(m,n)')
    def iterate_mandelbrot(c_re, c_im, it_count):

        apply_smoothening = True # trigger for applying smooth color algorithm or not

        m, n = c_re.shape

        for i in range(m):
            for j in range(n):
                re = 0
                im = 0
                count = iterate_max
                for it_n in xrange(iterate_max + 1):
                    xx = re * re
                    yy = im * im
                    xy = re * im
                    re = xx - yy + c_re[i,j]
                    im = 2 * xy + c_im[i,j]
                    if (xx+yy) > iteration_bound:
                        count = it_n
                        break

                if count < iterate_max and apply_smoothening:
                    log_zn = np.log( xx + yy ) * .5
                    nu = np.log(log_zn / np.log(2)) / np.log(2)
                    count += 1 - nu

                it_count[i,j] = count

    t0 = time.clock()

    # Draw our image
    x, y = np.meshgrid(np.linspace(x0, x0 + xw, x_res,dtype=np.float64), np.linspace(y0, y0 + yw, y_res,dtype=np.float64))
    it_count = np.zeros(x.shape,dtype=np.float64)
    print "calling iterate_mandelbrot."
    iterate_mandelbrot(x,y,it_count)
    print "elapsed time:"+str(time.clock()-t0)+" sec"

    return it_count