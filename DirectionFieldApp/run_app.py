__author__ = 'benjamin'

import directions_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/directions/")
@object_page("directions")
def make_directions():
    app = directions_app.DirectionsApp.create()
    return app

