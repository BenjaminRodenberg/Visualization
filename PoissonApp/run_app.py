import pde_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/pde/")
@object_page("pde")
def make_ode():
    app = pde_app.PDEApp.create()
    return app
