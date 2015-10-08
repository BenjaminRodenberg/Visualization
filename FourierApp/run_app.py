__author__ = 'benjamin'

import fourier_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/fourier/")
@object_page("fourier")
def make_ode():
    app = fourier_app.FourierApp.create()
    return app

