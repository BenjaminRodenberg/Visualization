from MinimalInteractive import minimal_app
from ODEApp import ode_app
from FourierApp import fourier_app
from BoundaryValApp import boundaryVal_app
from ConvolutionApp import convolution_app
from DirectionFieldApp import directions_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page


@bokeh_app.route("/bokeh/minimal/")
@object_page("minimal")
def make_minimal():
    app = minimal_app.MinApp.create()
    return app


@bokeh_app.route("/bokeh/ode/")
@object_page("ode")
def make_ode():
    app = ode_app.ODEApp.create()
    return app


@bokeh_app.route("/bokeh/fourier/")
@object_page("fourier")
def make_fourier():
    app = fourier_app.FourierApp.create()
    return app


@bokeh_app.route("/bokeh/boundary/")
@object_page("boundary")
def make_boundary():
    app = boundaryVal_app.BoundaryValApp.create()
    return app

@bokeh_app.route("/bokeh/convolution/")
@object_page("convolution")
def make_convolution():
    app = convolution_app.ConvolutionApp.create()
    return app

@bokeh_app.route("/bokeh/directions/")
@object_page("directions")
def make_direction():
    app = directions_app.DirectionsApp.create()
    return app



