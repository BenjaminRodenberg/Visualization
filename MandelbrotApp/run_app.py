import mandelbrot_app

from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

@bokeh_app.route("/bokeh/mandel/")
@object_page("mandel")
def make_mandel():
    app = mandelbrot_app.MandelbrotApp.create()
    return app
