import ode_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/ode/")
@object_page("ode")
def make_ode():
    app = ode_app.ODEApp.create()
    return app
