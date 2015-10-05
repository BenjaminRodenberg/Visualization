import minimal_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/minimal/")
@object_page("minimal")
def make_minimal():
    app = minimal_app.MinApp.create()
    return app