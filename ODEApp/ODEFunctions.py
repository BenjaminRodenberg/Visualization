# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:57:55 2015

@author: benjamin
"""

import numpy as np
import scipy as sp
#import matplotlib as mpl
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
