# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 18:03:09 2015

@author: benjamin
"""

import numpy as np
import math
from scipy.integrate import quad

#==============================================================================
# Here the function, of which we calculate the fourier series, is hardcoded if 
# one wants to use a different function, this has to be changed here.
#==============================================================================
def f( x ):
    return saw(x);

#==============================================================================
# The hat function    
#==============================================================================
def hat(x):    
    if x < np.pi:
        y = x/np.pi
    else:
        y = (2*np.pi-x)/np.pi      
    return y

#==============================================================================
# The step function
#==============================================================================
def step(x):
    if x < np.pi:
        y = -1.0
    else:
        y = 1.0      
    return y

#==============================================================================
# The sawtooth function    
#==============================================================================
def saw(x):
    if x < np.pi:
        y = x-np.pi/2
    else:
        y = x-3*np.pi/2
    return y

#==============================================================================
# This function computes the coefficients of the fourier series representation
# of the function f, which is periodic on the interval [start,end] up to the 
# degree N.   
#==============================================================================
def coeff(f,start,end,N):
    T=end-start
    a = (N+1) * [0]
    b = (N+1) * [0]
    
    for k in range(0,N+1):
        tmp=quad(lambda x: 2/T*f(x)*math.cos(2*math.pi*k*x/T),start,end)
        a[k]=tmp[0]
        tmp=quad(lambda x: 2/T*f(x)*math.sin(2*math.pi*k*x/T),start,end)
        b[k]=tmp[0]
        
    a[0]=a[0]/2        
    
    return[a,b]
    
#==============================================================================
# This function evaluates the fourier series of degree N with the coefficient
# vectors a and b and the period length T at the points in the array x.
#==============================================================================
def fourier_series(a,b,T,x):
    N = len(a)-1
    y = 0
    for k in range(0,N+1):
        y += a[k]*math.cos(2*math.pi*k*x/T)+b[k]*math.sin(2*math.pi*k*x/T)
    
    return y