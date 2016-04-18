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

c_heat = pde_constants.heat_conductivity
c_wave = pde_constants.wave_number


def heat_analytical(f0,x,t):

    u0 = f0(x)

    u = u0[0] * (x-np.max(x))/(np.max(x)-np.min(x)) + u0[-1] * (x-np.min(x))/(np.max(x)-np.min(x))
    u0 -= u
    u0 = np.concatenate([u0,-u0[-2::-1]]) # periodically extend function

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
    u += np.sum(np.exp(-(kk**2)*(c_heat ** 2)*t) * (b * np.sin(np.outer(x,kk)) + a * np.cos(np.outer(x,kk))), axis=1)

    u -= a[0] / 2
    return u


def wave_analytical(f0,x,t):

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
    u += np.sum(np.cos(kk * t * c_wave) * (b * np.sin(np.outer(x,kk)) + a * np.cos(np.outer(x,kk))), axis=1)
    return u
