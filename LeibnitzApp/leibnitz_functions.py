"""
Created on Thu Jul 30 18:03:09 2015

@author: benjamin
"""

import numpy as np
from sympy import sympify, lambdify
from sympy.core import diff
from scipy.integrate.quadpack import quad


def sym_parser(fun_str):
    fun_sym = sympify(fun_str)
    return fun_sym


def parser(fun_str):
    from sympy.abc import t

    fun_sym = sym_parser(fun_str)
    fun_lam = lambdify(t, fun_sym,['numpy'])
    return fun_lam


def calc_area(f_x_str,f_y_str, t_val):
    from sympy.abc import t
    f_x_sym = sym_parser(f_x_str)
    f_y_sym = sym_parser(f_y_str)

    f_x = lambdify(t, f_x_sym,['numpy'])
    f_y = lambdify(t, f_y_sym, ['numpy'])
    df_x = lambdify(t, diff(f_x_sym), ['numpy'])
    df_y = lambdify(t, diff(f_y_sym), ['numpy'])

    integrand = lambda tau: f_x(tau)*df_y(tau)-df_x(tau)*f_y(tau)
    return abs(0.5 * quad(integrand, 0, t_val)[0])
