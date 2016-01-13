# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 18:03:09 2015

@author: benjamin
"""

import numpy as np
import math

from Cython.Shadow import array
from scipy.integrate import quad


#==============================================================================
# The window function
#==============================================================================
from sqlalchemy.dialects.postgresql.base import array


def window(x):
    return np.piecewise(x,
                        [x < -.5,
                         (-.5 <= x) * (x <= .5),
                         .5 < x],
                        [0,
                         1,
                         0])

#==============================================================================
# The ramp function
#==============================================================================
def ramp(x):
    return np.piecewise(x,
                        [x < 0,
                         (0 <= x) * (x <= 1.0),
                         1.0 < x],
                        [lambda arg: 0.0,
                         lambda arg: arg,
                         lambda arg: 0.0])

def saw(x):
    w = 2.0 # intervall width
    n = 2 # number of oszillations
    return (((x+w*.5)%w) - w*.5) * npHeaviside(x+w*n*.5) * npHeaviside(w*n*.5-x)


def npHeaviside(x):
    """
    numpy compatible implementation of heaviside function
    :param x: ndarray
    :return: ndarray
    """
    return np.piecewise(x,
                        [x<0,
                         x==0,
                         x>0],
                        [lambda arg: 0.0,
                         lambda arg: 0.5,
                         lambda arg: 1.0])

def npDirac(x, h):
    """
    numpy compatible implementation of dirac delta. This implementation is representing a disrete version of dirac with
    width h and height 1/h. Area under dirac is equal to 1.
    :param x: ndarray, evaluation point
    :param h: width of dirac
    :return: ndarray
    """
    return npHeaviside(x)*npHeaviside(h-x)*1.0/h

#==============================================================================
# parses a function with given fun_str and returns lambda function
#==============================================================================
def parser(fun_str, h):
    from sympy import sympify, lambdify
    from sympy.abc import x

    print "parsing:"
    print "\tstring:\t"+str(fun_str)
    fun_sym = sympify(fun_str)
    print "\tsymbolic:\t"+str(fun_sym)
    fun_lam = lambdify(x, fun_sym,['numpy',
                                   {"Heaviside": npHeaviside},
                                   {"Dirac": lambda x: npDirac(x,h)}])
    print "\tfunction:\t"+str(fun_lam)

    return fun_lam


def compute_overlay_vector(y1,y2):
    assert(y1.size == y2.size)

    N = y1.size
    y_positive = np.zeros(2 * y1.size)
    y_negative = np.zeros(2 * y1.size)

    for i in range(N):
        if y1[i] * y2[i] > 0:
            if y1[i] < y2[i]:
                if y1[i] > 0:
                    y_positive[i] = y1[i]
                else:
                    y_positive[i] = y2[i]
            else:
                if y2[i] > 0:
                    y_positive[i] = y2[i]
                else:
                    y_positive[i] = y1[i]
        elif y1[i] * y2[i] < 0:
            if abs(y1[i]) > abs(y2[i]):
                y_negative[i] = -abs(y2[i])
                y_negative[2*N-i-1] = 0#y1[i]
            else:
                y_negative[i] = -abs(y1[i])
                y_negative[2*N-i-1] = 0#y2[i]

    return y_positive, y_negative


def find_interval(x_array, x_value):
    """
    finds the interval in an ascending ordered array, in which the value lies using bisection
    :param x_array: ascending ordered nparray a[0...N-1]
    :param x_value: value x
    :return i_left: index defining lower and upper bound of the interval such that a[i]<x<a[i+1]
    """
    assert(type(x_array) is np.ndarray or type(x_array) is list)
    if x_array is list:
        x_array = np.array(x_array)
    assert(x_array.ndim == 1)

    i_left = 0
    i_right = int(x_array.__len__() - 1)

    while i_left+1 < i_right:
        print str(i_left)+"|"+str(i_right)
        assert(x_array[i_left] <= x_value <= x_array[i_right])

        i_middle = int(np.floor((i_left + i_right)*.5))
        print str(i_middle)

        if x_array[i_middle] <= x_value:
            i_left = i_middle
        else:
            i_right = i_middle

    return i_left


def find_value(x_array, y_array, x_value):
    """
    Calculates the y value corresponding to a given x value for two corresponding data arrays in x and y using linear
    interpolation.
    :param x_array: with datapoints in ascending order
    :param y_array: with values corresponding to datapoints in array_y
    :param x_value: not necessarily in array_x
    :return y_value: corresponding to x value computed via linear interpolation
    """

    idx = find_interval(x_array, x_value)

    x_left = x_array[idx]
    x_right = x_array[idx + 1]

    # now use the following linear interpolation formula: (1-t) * x_left + t * x_right = x_value
    # t is the parameter in [0,1] corresponding to value_x
    t = float((x_value - x_left)) / float((x_right - x_left))

    y_left = y_array[idx]
    y_right = y_array[idx + 1]
    y_value = (1-t) * y_left + t * y_right

    return y_value



