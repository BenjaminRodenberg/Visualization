from __future__ import division
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


def calculate_arrow_data(x, y, u, v):
    def quiver_to_segments(x, y, u, v):
        x = x.flatten()
        y = y.flatten()
        u = u.flatten()
        v = v.flatten()

        x0 = x
        y0 = y
        x1 = x + u
        y1 = y + v

        return x0, y0, x1, y1

    def quiver_to_arrowheads(x, y, u, v):

        def __t_matrix(translate_x, translate_y):
            return np.array([[1, 0, translate_x],
                             [0, 1, translate_y],
                             [0, 0, 1]])

        def __r_matrix(rotation_angle):
            c = np.cos(rotation_angle)
            s = np.sin(rotation_angle)
            return np.array([[c, -s, 0],
                             [s, +c, 0],
                             [0, +0, 1]])

        def __head_template(x0, y0, u, v, type_id, headsize):
            if type_id is 0:
                x_patch = 3 * [None]
                y_patch = 3 * [None]

                x1 = x0 + u
                x_patch[0] = x1
                x_patch[1] = x1 - headsize
                x_patch[2] = x1 - headsize

                y1 = y0 + v
                y_patch[0] = y1
                y_patch[1] = y1 + headsize / np.sqrt(3)
                y_patch[2] = y1 - headsize / np.sqrt(3)
            elif type_id is 1:
                x_patch = 4 * [None]
                y_patch = 4 * [None]

                x1 = x0 + u
                x_patch[0] = x1
                x_patch[1] = x1 - headsize
                x_patch[2] = x1 - headsize / 2
                x_patch[3] = x1 - headsize

                y1 = y0 + v
                y_patch[0] = y1
                y_patch[1] = y1 + headsize / np.sqrt(3)
                y_patch[2] = y1
                y_patch[3] = y1 - headsize / np.sqrt(3)
            else:
                raise Exception("unknown head type!")

            return x_patch, y_patch

        def __get_patch_data(x0, y0, u, v, headsize):

            def angle_from_xy(x, y):
                if x == 0:
                    return np.pi * .5 + int(y <= 0) * np.pi
                else:
                    if y >= 0:
                        if x > 0:
                            return np.arctan(y / x)
                        elif x < 0:
                            return -np.arctan(y / -x) + np.pi
                        else:
                            return 1.5*np.pi
                    else:
                        if x > 0:
                            return -np.arctan(-y / x)
                        elif x < 0:
                            return np.arctan(-y / -x) + np.pi
                        else:
                            return .5*np.pi

            angle = angle_from_xy(u, v)

            x_patch, y_patch = __head_template(x0, y0, u, v, type_id=1, headsize=headsize)

            T1 = __t_matrix(-x_patch[0], -y_patch[0])
            R = __r_matrix(angle)
            T2 = __t_matrix(x_patch[0], y_patch[0])
            T = T2.dot(R.dot(T1))

            for i in range(x_patch.__len__()):
                v_in = np.array([x_patch[i], y_patch[i], 1])
                v_out = T.dot(v_in)
                x_patch[i], y_patch[i], tmp = v_out

            return x_patch, y_patch

        x = x.flatten()
        y = y.flatten()
        u = u.flatten()
        v = v.flatten()

        n_arrows = x.shape[0]
        xs = n_arrows * [None]
        ys = n_arrows * [None]

        headsize = .05 * (u**2 + v**2)

        for i in range(n_arrows):
            x_patch, y_patch = __get_patch_data(x[i], y[i], u[i], v[i], headsize)
            xs[i] = x_patch
            ys[i] = y_patch

        return xs, ys

    x0, y0, x1, y1 = quiver_to_segments(x, y, u, v)
    segments = dict(x0=x0, y0=y0, x1=x1, y1=y1)

    xs, ys = quiver_to_arrowheads(x, y, u, v)
    patches = dict(xs=xs, ys=ys)

    return segments, patches


def calculate_tangent(f_x_str, f_y_str, t0):
    f_x_sym = sym_parser(f_x_str)
    f_y_sym = sym_parser(f_y_str)
    f_x = parser(f_x_str)
    f_y = parser(f_y_str)

    from sympy.core import diff
    from sympy.abc import t

    df_x_sym = diff(f_x_sym)
    df_y_sym = diff(f_y_sym)
    df_x = lambdify(t, df_x_sym, ['numpy'])
    df_y = lambdify(t, df_y_sym, ['numpy'])

    x = np.array([f_x(t0)])
    y = np.array([f_y(t0)])
    u = np.array([df_x(t0)])
    v = np.array([df_y(t0)])

    return x,y,u,v


def normalize(u,v):
    l = np.sqrt(u**2 + v**2)
    u = u / l
    v = v / l
    return u,v


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