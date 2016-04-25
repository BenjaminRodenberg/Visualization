from __future__ import division
import numpy as np


# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
pde_constants = import_bokeh('pde_constants.py')


def heat_analytical(f0, x, t):
    '''
    wrapper function for calling the appropriate analytical solution scheme.
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param x: spatial x values for evaluation
    :param t: time t
    :return: solution of heat transport equation at time t at positions x
    '''
    t+=.01 # artificial addition to time for avoiding Gibbs phenomenom
    c_heat = pde_constants.heat_conductivity
    u_xt = heat_fourier(f0, c_heat, x, t)
    return u_xt


def heat_fourier(f0, c_heat, x, t):
    '''
    computes the analytical solution for the heat transport equation in 1D using fourier series ansatz. The fourier
    series approximation of the initial condition is computed using fast fourier transform.
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param c_heat: heat transport coefficient
    :param x: spatial x values for evaluation (equally spaced!)
    :param t: time t
    :return: u: solution of heat transport equation at time t at positions x
    '''

    u0 = f0(x)

    u = u0[0] * (x - np.max(x)) / (np.max(x) - np.min(x)) + u0[-1] * (x - np.min(x)) / (np.max(x) - np.min(x))
    u0 -= u
    u0 = np.concatenate([u0, -u0[-2::-1]])  # periodically extend function

    K = u0.__len__()

    c = np.fft.fft(u0)

    b = -2 * np.imag(c) / K
    a = 2 * np.real(c) / K
    K = int(K / 2) + 1
    b = b[:K]
    a = a[:K]

    w = np.max(x) - np.min(x)

    # numpy matrix version of code below
    """
    for k in range(K):
        kk = k * np.pi / w
        u += np.exp(-(kk**2)*(c_heat ** 2)*t) * (b[k] * np.sin(kk*x) + a[k] * np.cos(kk*x))
    """
    k = np.arange(K)
    kk = k * np.pi / w
    u += np.sum(np.exp(-(kk ** 2) * (c_heat ** 2) * t) * (b * np.sin(np.outer(x, kk)) + a * np.cos(np.outer(x, kk))),
                axis=1)

    u -= a[0] / 2
    return u


def wave_analytical(f0, x, t):
    '''
    wrapper function for calling the appropriate analytical solution scheme.
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param x: spatial x values for evaluation
    :param t: time t
    :return: solution of wave equation at time t at positions x
    '''
    c_wave = pde_constants.wave_number
    u_xt = wave_dAlembert(f0, c_wave, x, t)
    return u_xt


def wave_fourier(f0, c_wave, x, t):
    '''
    computes the analytical solution for the wave equation in 1D using fourier series ansatz. The fourier
    series approximation of the initial condition is computed using fast fourier transform. The initial condition f0' is
    assumed to be equal to zero. For theory see 'Karpfinger: Rezepte'
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param c_wave: wave travelling speed
    :param x: spatial x values for evaluation (equally spaced!)
    :param t: time t
    :return: u: solution of wave equation at time t at positions x
    '''

    u0 = f0(x)

    u = u0[0] * (x - np.max(x)) / (np.max(x) - np.min(x)) + u0[-1] * (x - np.min(x)) / (np.max(x) - np.min(x))
    u0 -= u
    u0 = np.concatenate([u0, -u0[-2::-1]])  # periodically extend function

    K = u0.__len__()

    c = np.fft.fft(u0)

    b = -2 * np.imag(c) / K
    a = 2 * np.real(c) / K
    K = int(K / 2) + 1
    b = b[:K]
    a = a[:K]

    w = np.max(x) - np.min(x)

    # numpy matrix version of code below
    """
    for k in range(K):
        kk = k * np.pi / w
        u += np.cos(kk * t  * c_wave) * (b[k] * np.sin(kk*x) + a[k] * np.cos(kk*x))
    """
    k = np.arange(K)
    kk = k * np.pi / w
    u += np.sum(np.cos(kk * t * c_wave) * (b * np.sin(np.outer(x, kk)) + a * np.cos(np.outer(x, kk))), axis=1)
    return u


def wave_dAlembert(f0, c_wave, x, t):
    '''
    computes the analytical solution for the wave equation in 1D using d'Alemberts ansatz. The initial condition f0' is
    assumed to be equal to zero.
    http://www.jirka.org/diffyqs/htmlver/diffyqsse32.html
    :param f0: analytical, functional expression for the initial condition, that can be evaluated for arbitrary x
    :param c_wave: wave travelling speed
    :param x: spatial x values for evaluation
    :param t: time t
    :return: u_xt: solution of wave equation at time t at positions x
    '''
    w = np.max(x) - np.min(x)

    x_r = (x - c_wave * t)%(2*w)
    x_l = (x + c_wave * t)%(2*w)
    sign_r = np.where((x_r > w),-1,1)
    sign_l = np.where((x_l > w),-1,1)
    x_r[x_r > w] = 2 * w - x_r[x_r > w]
    x_l[x_l > w] = 2 * w - x_l[x_l > w]

    u_r = (sign_r * f0(x_r))
    u_l = (sign_l * f0(x_l))
    u_xt = (u_r + u_l)*.5

    return u_xt


