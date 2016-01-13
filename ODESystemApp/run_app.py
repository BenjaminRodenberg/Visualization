__author__ = 'benjamin'

import odesystem_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/odesystem/")
@object_page("odesystem")
def make_odesystem():
    app = odesystem_app.ODESystemApp.create()
    return app

