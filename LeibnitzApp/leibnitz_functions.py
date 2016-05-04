"""
Created on Thu Jul 30 18:03:09 2015

@author: benjamin
"""

import numpy as np

def parser(fun_str):
    from sympy import sympify, lambdify
    from sympy.abc import t

    fun_sym = sympify(fun_str)
    fun_lam = lambdify(t, fun_sym,['numpy'])
    return fun_lam