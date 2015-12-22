from __future__ import division

import numpy as np

from bokeh.plotting import figure, show, output_file

import quiver

__author__ = 'benjamin'

def logistic_function(x,coeff):
    a, b = coeff
    return a * x - b * x**2

h = .05
xx = np.arange(-1.5, 1.5+h, h)
yy = np.arange(-1.5, 1.5+h, h)

a, b = [0, 8]
coeff = [a, b]

Y, X = np.meshgrid(xx, yy)
U = np.ones(X.shape)
V = logistic_function(Y, coeff)

output_file("vector.html", title="vector.py example")

p1 = figure()
p1.quiver(x=X, y=Y, u=U, v=V)
p1.line([X[0,1],X[-1,1]],[a/b,a/b],color='red')
p1.line([X[0,1],X[-1,1]],[0,0],color='red')

show(p1)  # open a browser
