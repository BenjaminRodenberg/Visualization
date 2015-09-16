# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging

logging.basicConfig(level=logging.DEBUG)

import ode_functions as ode_fun

from bokeh.models.widgets import HBox, Slider, RadioButtonGroup, VBoxForm, Dropdown
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.plotting import figure
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.embed import components


class ODEApp(HBox):
    # ==============================================================================
    # Only bokeh quantities for layout, data, controls... go here!
    # ==============================================================================
    extra_generated_classes = [["ODEApp", "ODEApp", "HBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    startvalue = Instance(Slider)
    stepsize = Instance(Slider)
    solvers = Instance(RadioButtonGroup)
    odes = Instance(RadioButtonGroup)
    #solvers = Instance(Dropdown)
    #odes = Instance(Dropdown)

    # plot
    plot = Instance(Plot)

    # data
    source = Instance(ColumnDataSource)
    source_ref = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # default values
        timespan = 5
        x0 = 1
        h = 1

        # initialize data source
        obj.source = ColumnDataSource(data=dict(t=[], x=[]))
        obj.source_ref = ColumnDataSource(data=dict(t_ref=[], x_ref=[]))

        # initialize controls
        # slider controlling stepsize of the solver
        obj.stepsize = Slider(
            title="stepsize", name='stepsize',
            value=h, start=0.1, end=1.0, step=.05
        )
        # slider controlling initial value of the ode
        obj.startvalue = Slider(
            title="startvalue", name='startvalue',
            value=x0, start=0, end=2, step=.1
        )
        # gives the opportunity to choose from different solvers
        obj.solvers = RadioButtonGroup(
            labels=["ExplicitEuler", "ImplicitEuler", "MidpointRule"], active=0
        )
        #obj.solvers = Dropdown(label="solvers",type="warning",menu=[("ExplicitEuler","0"),("ImplicitEuler","1"),("MidpointRule","2")])
        # gives the opportunity to choose from different odes
        obj.odes = RadioButtonGroup(
            labels=["Dahlquist", "Logistic"], active=0
        )
        #obj.odes = Dropdown(label="ODE",type="warning",menu=[("Dahlquist","0"),("Logistic","1")])

        # initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      # title=obj.text.value,
                      title="numerical ODE solving",
                      x_range=[0, timespan],
                      y_range=[-1.5, 3.5]
                      )
        # Plot the numerical solution by the x,t values in the source property
        plot.line('t', 'x', source=obj.source,
                  line_width=.5,
                  line_alpha=0.6,
                  color='red',
                  line_dash=[4, 4]
                  )
        plot.circle('t','x',source=obj.source,
                    color='red',
                    legend='numerical solution'
                    )
        # Plot the analytical solution by the x_ref,t values in the source property
        plot.line('t_ref', 'x_ref', source=obj.source_ref,
                  color='green',
                  line_width=3,
                  line_alpha=0.6,
                  legend='analytical solution'
                  )
        obj.plot = plot
        # calculate data
        obj.update_data()

        # lists all the controls in our app
        obj.controls = VBoxForm(
            children=[
                obj.stepsize, obj.startvalue, obj.solvers, obj.odes
            ]
        )

        # make layout
        obj.children.append(obj.controls)
        obj.children.append(obj.plot)

        # don't forget to return!
        return obj

    def setup_events(self):
        # ==============================================================================
        # Here we have to set up the event behaviour.
        # ==============================================================================
        # recursively searches the right level?
        if not self.startvalue:
            return

        # event registration
        self.stepsize.on_change('value', self, 'input_change')
        self.startvalue.on_change('value', self, 'input_change')
        self.solvers.on_change('active', self, 'input_change')
        self.odes.on_change('active', self, 'input_change')

    def input_change(self, obj, attrname, old, new):
        # ==============================================================================
        # This function is called if input changes
        # ==============================================================================
        print "input changed!"
        self.update_data()

    def update_data(self):
        # ==============================================================================
        # Updated the data respective to input
        # ==============================================================================

        # default values for ODEs...
        k = 5
        g = .5
        lam = -5
        timespan = 5.0
        # available ODEs
        ode_library = [lambda t, x: ode_fun.dahlquist(t, x, lam),
                       lambda t, x: ode_fun.logistic_equation(t, x, k, g)]
        # respective reference solutions
        ref_library = [lambda t, x0: ode_fun.dahlquist_ref(t, x0, lam),
                       lambda t, x0: ode_fun.logistic_equation_ref(t, x0, k, g)]

        # available solvers
        solver_library = [lambda f, x0, h, timespan: ode_fun.expl_euler(f, x0, h, timespan),
                          lambda f, x0, h, timespan: ode_fun.impl_euler(f, x0, h, timespan),
                          lambda f, x0, h, timespan: ode_fun.impl_midpoint(f, x0, h, timespan)]

        # Get the current slider values
        h = self.stepsize.value;
        x0 = self.startvalue.value;
        solver = solver_library[self.solvers.active]
        ode = ode_library[self.odes.active]
        ref = ref_library[self.odes.active]

        # solve ode with numerical scheme        
        [t, x] = solver(ode, x0, h, timespan)
        [t_ref, x_ref] = ode_fun.ref_sol(ref, x0, timespan)

        # save data
        x = x.tolist()
        t = t.tolist()
        x_ref = x_ref.tolist()
        t_ref = t_ref.tolist()
        self.source.data = dict(t=t, x=x)
        self.source_ref.data = dict(x_ref=x_ref, t_ref=t_ref)

        print "data was updated with parameters: h=" + str(h) + " and x0=" + str(x0)


@bokeh_app.route("/bokeh/ode/")
@object_page("blabla")
def make_ode():
    app = ODEApp.create()
    return app
