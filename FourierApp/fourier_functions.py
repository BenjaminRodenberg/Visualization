import numpy as np
import math
from scipy.integrate import quad

#==============================================================================
# The hat function    
#==============================================================================
def hat(x):
    return npHeaviside(x) * (np.pi+x)/np.pi + npHeaviside(-1*x) * (np.pi-x)/np.pi

#==============================================================================
# The step function
#==============================================================================
def step(x):
    return npHeaviside(x) - npHeaviside(-1*x)

#==============================================================================
# The sawtooth function    
#==============================================================================
def saw(x):
    return x/np.pi


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


def parser(fun_str):
    from sympy import sympify, lambdify
    from sympy.abc import x

    fun_sym = sympify(fun_str)
    fun_lam = lambdify(x, fun_sym,['numpy',
                                   {"Heaviside": npHeaviside},
                                   {"Dirac": npDirac}])
    return fun_lam


def number_parser(number_str):
    from sympy import sympify
    number_sym = sympify(number_str)
    return float(number_sym)


#==============================================================================
# This function computes the coefficients of the fourier series representation
# of the function f, which is periodic on the interval [start,end] up to the 
# degree N.   
#==============================================================================
def coeff(f, start, end, N):
    T = end-start
    a = (N+1) * [0]
    b = (N+1) * [0]
    
    for k in range(0, N+1):
        tmp_fun = lambda x: 2/T*f(np.asarray([x]))*np.cos(2*math.pi*k*x/T)
        tmp = quad(tmp_fun, start, end)
        a[k] = tmp[0]
        print "a[%d] = %f" % (k,a[k])
        tmp_fun = lambda x: 2/T*f(np.asarray([x]))*np.sin(2*math.pi*k*x/T)
        tmp = quad(tmp_fun, start, end)
        b[k] = tmp[0]
        print "b[%d] = %f" % (k,b[k])
        
    a[0] = a[0] / 2
    
    return [a, b]
    
#==============================================================================
# This function evaluates the fourier series of degree N with the coefficient
# vectors a and b and the period length T at the points in the array x.
#==============================================================================
def fourier_series(a, b, T, x):
    N = len(a)-1
    y = 0
    for k in range(0, N+1):
        y += a[k]*math.cos(2*math.pi*k*x/T)+b[k]*math.sin(2*math.pi*k*x/T)
    
    return y