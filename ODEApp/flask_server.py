from __future__ import print_function

import logging
logging.basicConfig(level=logging.INFO)

from bokeh.pluginutils import app_document
from flask import Flask, render_template

from ode_app import ODEApp

app = Flask('sampleapp')

bokeh_url = "http://localhost:5006"
applet_url = "http://localhost:5050"

@app_document("ode_example", bokeh_url)
def make_ode_applet():
    app = ODEApp.create()
    return app

@app.route("/")
def applet():
    applet = make_ode_applet()
    return render_template(
        "ode.html",
        app_url = bokeh_url + "/bokeh/jsgenerate/HBox/ODEApp/ODEApp",
        app_tag = applet._tag
    )

if __name__ == "__main__":
    print("\nView this example at: %s\n" % applet_url)
    app.debug = True
    app.run(host='0.0.0.0', port=5050)
