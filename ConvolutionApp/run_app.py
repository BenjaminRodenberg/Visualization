__author__ = 'benjamin'

import convolution_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/convolution/")
@object_page("convolution")
def make_ode():
    app = convolution_app.ConvolutionApp.create()
    return app

