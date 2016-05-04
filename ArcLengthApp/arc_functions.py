from sympy import sympify, lambdify
from sympy.core import diff
from scipy.integrate.quadpack import quad
from scipy.optimize import newton
import numpy as np

def sym_parser(fun_str):
    fun_sym = sympify(fun_str)
    return fun_sym

def parser(fun_str):
    from sympy.abc import t

    fun_sym = sym_parser(fun_str)
    fun_lam = lambdify(t, fun_sym,['numpy'])
    return fun_lam


def arclength(df_x, df_y, t):
    integrand = lambda tau: np.sqrt( df_x(tau)**2+df_y(tau)**2 )
    return quad(integrand,0,t)[0]


def s_inverse(df_x, df_y, t):
    s = lambda tau: arclength(df_x,df_y,tau)-t # objective function
    return newton(s,0)


def central_finite_difference(f,h,x0):
    return (f(x0+h)-f(x0-h)) / (2.0*h)

f_x_str = 't**2'
f_y_str = 'cos(t)'

f_x_sym = sym_parser(f_x_str)
f_y_sym = sym_parser(f_y_str)

df_x_sym = diff(f_x_sym)
df_y_sym = diff(f_y_sym)

from sympy.abc import t
df_x = lambdify(t, df_x_sym,['numpy'])
df_y = lambdify(t, df_y_sym,['numpy'])

f_x = lambdify(t, f_x_sym, ['numpy'])
f_y = lambdify(t, f_y_sym, ['numpy'])

gamma_x = lambda t: f_x(s_inverse(df_x,df_y,t))
gamma_y = lambda t: f_y(s_inverse(df_x,df_y,t))

t0 = 1.0
t0_non_arc = s_inverse(df_x,df_y,t0)

n_x_non_arc = central_finite_difference(f_x,.00001,t0_non_arc)
n_y_non_arc = central_finite_difference(f_y,.00001,t0_non_arc)

n_x = central_finite_difference(gamma_x,.00001,t0)
n_y = central_finite_difference(gamma_y,.00001,t0)

n_abs = n_x**2+n_y**2

n_abs_non_arc = n_x_non_arc**2+n_y_non_arc**2