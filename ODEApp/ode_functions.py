# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:57:55 2015

@author: benjamin
"""

import numpy as np
import scipy as sp
from scipy.optimize import newton
from scipy.optimize import fsolve


def dahlquist(t, x, lam): # dahlquist test equation
    dx = lam * x
    return dx


def dahlquist_ref(t, x0, lam):
    x_ref = sp.exp(lam * t) * x0  # analytical solution of the dahlquist test equation
    return x_ref


def definition_area(t, x):  # for the initial value x0 = 1 this ODE only has a solution for x in (-sqrt(2),sqrt(2)).
    dx = t * x ** 2
    return dx


def definition_area_ref(t, x0):
    x_ref = 1. / (1. / x0 - 1. / 2. * (t ** 2))  # analytical solution of this ODE
    return x_ref


def logistic_equation(t, x, k, g):
    dx = k * x * (g - x)
    return dx


def logistic_equation_ref(t, x0, k, G):
    if 0 != x0:
        x_ref = G * 1 / (1 + np.exp(-k * G * t) * (G / x0 - 1))
    else:
        x_ref = 0
    return x_ref


def oscillator_equation(t, x, omega):
    A = np.array([[0,1],[-omega**2,0]])
    dx = np.dot(A,x)
    return dx


def oscillator_equation_ref(t, x0, omega):
    x = x0[0]*np.exp(1j*omega*t)+ x0[1]*np.exp(-1j*omega*t)
    return float(np.real(x))


def ref_sol(f_ref,x0,timespan):
    h = float(timespan) / 1000.0
    n = int(np.ceil(timespan / h))
    t_ref = np.empty(n + 1)
    x_ref = np.empty(n + 1)

    t_ref[0] = 0
    x_ref[0] = x0[0]
    for k in range(n):
        t_ref[k + 1] = (k + 1) * h
        x_ref[k + 1] = f_ref(t_ref[k + 1], x0)

    return t_ref, x_ref


def expl_euler(f, x0, h, timespan):
    n = int(np.ceil(timespan / h))
    t = np.empty(n + 1)
    x = np.empty([x0.shape[0], n + 1])

    t[0] = 0
    x[:,0] = x0
    for k in range(n):
        dx = f(t[k], x[:,k])
        t[k + 1] = (k + 1) * h
        x[:,k + 1] = x[:,k] + dx * h

    return t, x


def impl_euler(f, x0, h, timespan):
    n = int(np.ceil(timespan / h))
    t = np.empty(n + 1)
    x = np.empty([x0.shape[0], n + 1])

    t[0] = 0
    x[:, 0] = x0
    for k in range(n):
        t[k + 1] = (k + 1) * h
        try:
            x[:, k + 1] = fsolve(lambda arg: x[:, k] - arg + h * f(t[k + 1], arg), x[:, k])
        except RuntimeError:
            print "newton did not converge!"
            for k in range(k, n):
                t[k + 1] = (k + 1) * h
            break
    return t, x


def impl_midpoint(f, x0, h, timespan):
    n = int(np.ceil(timespan / h))
    t = np.empty(n + 1)
    x = np.empty([x0.shape[0], n + 1])

    t[0] = 0
    x[:, 0] = x0
    for k in range(n):
        t[k + 1] = (k + 1) * h
        try:
            dx_left = f(t[k], x[:, k])
            x[:, k + 1] = fsolve(lambda arg: x[:, k] - arg + h / 2 * (f(t[k + 1], arg) + dx_left), x[:, k])
        except RuntimeError:
            print "newton did not converge!"
            for k in range(k, n):
                t[k + 1] = (k + 1) * h
            break
    return t, x