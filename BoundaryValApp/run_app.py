import boundaryVal_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page


@bokeh_app.route("/bokeh/boundary/")
@object_page("boundary")
def make_minimal():
    app = boundaryVal_app.BoundaryValApp.create()
    return app