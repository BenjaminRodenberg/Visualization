# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:57:55 2015

@author: benjamin
"""

import numpy as np
import scipy as sp
#import matplotlib as mpl
from bokeh.plotting import figure,output_file, show
from scipy.optimize import newton
#import math
#import bokeh.embed as embed

def dahlquist(t,x,x0,lam): #dahlquist test equation
    dx = lam*x;
    x_ref = sp.exp(lam*t)*x0; #analytical solution of the dahlquist test equation
    return dx,x_ref;
    
def definitionArea(t,x,x0): #for the initial value x0 = 1 this ODE only has a solution for x in (-sqrt(2),sqrt(2)).
    dx = t*x**2;    
    x_ref = 1./(1./x0-1./2.*(t**2)); #analytical solution of this ODE
    return dx,x_ref;
    
def logisticEquation(t,x,x0,k,G):
    dx = k * x * (G-x);
    if x0 != 0:
        x_ref = G * 1/(1+np.exp(-k*G*t)*(G/x0-1));
    else:
        x_ref = 0;
            
    return dx,x_ref;

def explEuler(f,x0,h,T) :
    N=int(np.ceil(T/h));
    t=np.empty(N+1);
    x=np.empty(N+1);
    x_ref=np.empty(N+1);
    
    t[0]=0;
    x[0]=x0;
    for k in range(N):        
        [dx,x_ref[k]]=f(t[k],x[k],x0);
        t[k+1]=(k+1)*h;
        x[k+1]=x[k]+dx*h;   
        
    [dx,x_ref[k+1]]=f(t[k+1],x[k+1],x0);
        
    return t,x,x_ref;
    
def implEuler(f,x0,h,T) :
    N=int(np.ceil(T/h));
    t=np.empty(N+1);
    x=np.empty(N+1);    
    x_ref=np.empty(N+1);
    
    t[0]=0;
    x[0]=x0;
    [dx,x_ref[0]]=f(t[0],x[0],x0);
    for k in range(N):
        t[k+1]=(k+1)*h; 
        try:
            x[k+1]=newton(lambda X:x[k]-X+h*f(t[k+1],X,x0)[0],x[k])        
        except RuntimeError:
            print "newton did not converge!";
            for k in range(k,N):
                t[k+1]=(k+1)*h;
            break;
        [dx,x_ref[k+1]]=f(t[k+1],x[k+1],x0)
        
    return t,x,x_ref;  

def implMidpoint(f,x0,h,T):
    N=int(np.ceil(T/h));
    t=np.empty(N+1);
    x=np.empty(N+1);    
    x_ref=np.empty(N+1);
    
    t[0]=0;
    x[0]=x0;
    [dx,x_ref[0]]=f(t[0],x[0],x0);
    for k in range(N):
        t[k+1]=(k+1)*h; 
        try:
            dxLeft = f(t[k],x[k],x0)[0];
            x[k+1]=newton(lambda X:x[k]-X+h/2*(f(t[k+1],X,x0)[0]+dxLeft),x[k])        
        except RuntimeError:
            print "newton did not converge!";
            for k in range(k,N):
                t[k+1]=(k+1)*h;
            break;
        [dx,x_ref[k+1]]=f(t[k+1],x[k+1],x0)
        
    return t,x,x_ref;      
#==============================================================================
# Inputs for dahlquist test equation        
#==============================================================================
#==============================================================================
# lam = -10;
# x0 = 1;
# h = .5;
# T = 2.5;
# #[t,x,x_ref]=implEuler(lambda t,x,x_0:dahlquist(t,x,x_0,lam),x0,h,T)
# #[t,x,x_ref]=explEuler(lambda t,x,x_0:dahlquist(t,x,x_0,lam),x0,h,T)
#==============================================================================

#==============================================================================
#  Inputs for function which is only defined in a certain area for certain x0
#==============================================================================
#==============================================================================
# x0 = 1; # no solution exists for x>=sqrt(2), if x0 = 1.
# h  = .1;
# T  = sp.sqrt(2)-10*h;
# #[t,x,x_ref]=explEuler(definitionArea,x0,h,T);
# #[t,x,x_ref]=implEuler(definitionArea,x0,h,T);
# #[t,x,x_ref]=implMidpoint(definitionArea,x0,h,T);
#==============================================================================

#==============================================================================
#  Inputs for logistic equation
#==============================================================================
#==============================================================================
# x0 = .1;
# h = 1;
# k = 1;
# G = 1;
# T = 10;
# #[t,x,x_ref]=explEuler(lambda t,x,x_0: logisticEquation(t,x,x_0,k,G),x0,h,T);
# 
# solver = implEuler;
# ODE = lambda t,x,x_0: logisticEquation(t,x,x_0,k,G);
# 
# [t,x,x_ref]=solver(ODE,x0,h,T);
# 
# # create a Figure object
# p = figure(width=300, height=300, tools="pan,reset,save,wheel_zoom");
# 
# x_plot = x.tolist();
# t_plot = t.tolist();
# x_ref_plot = x_ref.tolist();
# 
# # add a plot to this figure
# p.line(t_plot,x_plot,line_width=2)
# p.line(t_plot,x_ref_plot,line_width=2,color='red')
# # write figure to output
# output_file("foo.html")
#==============================================================================
# show figure
#show(p)





        