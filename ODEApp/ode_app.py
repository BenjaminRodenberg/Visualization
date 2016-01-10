# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging

logging.basicConfig(level=logging.DEBUG)

import ode_functions as ode_fun
import ode_settings

import numpy as np

from bokeh.models.widgets import HBox, Slider, RadioButtonGroup, VBoxForm, Dropdown
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.plotting import figure

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

        # initialize data source
        obj.source = ColumnDataSource(data=dict(t=[], x=[]))
        obj.source_ref = ColumnDataSource(data=dict(t_ref=[], x_ref=[]))

        # initialize controls
        # slider controlling stepsize of the solver
        obj.stepsize = Slider(
            title="stepsize", name='stepsize',
            value=ode_settings.step_init, start=ode_settings.step_min, end=ode_settings.step_max, step=ode_settings.step_step
        )
        # slider controlling initial value of the ode
        obj.startvalue = Slider(
            title="startvalue", name='startvalue',
            value=ode_settings.x0_init, start=ode_settings.x0_min, end=ode_settings.x0_max, step=ode_settings.x0_step
        )
        # gives the opportunity to choose from different solvers
        obj.solvers = RadioButtonGroup(
            labels=ode_settings.solver_labels, active=ode_settings.solver_init
        )
        # gives the opportunity to choose from different odes
        obj.odes = RadioButtonGroup(
            labels=ode_settings.odetype_labels, active=ode_settings.odetype_init
        )

        # initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      # title=obj.text.value,
                      title=ode_settings.title,
                      x_range=[ode_settings.min_time, ode_settings.max_time],
                      y_range=[ode_settings.min_y, ode_settings.max_y]
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
        obj.children.append(obj.plot)
        obj.children.append(obj.controls)

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
        k = ode_settings.logistic_k
        g = ode_settings.logistic_g
        lam = ode_settings.dahlquist_lambda
        timespan = ode_settings.max_time
        # available ODEs
        ode_library = ode_settings.ode_library
        # respective reference solutions
        ref_library = ode_settings.ref_library
        # available solvers
        solver_library = ode_settings.solver_library

        # Get the current slider values
        h = self.stepsize.value
        x0 = self.startvalue.value
        solver = solver_library[self.solvers.active]
        ode = ode_library[self.odes.active]
        ref = ref_library[self.odes.active]

        if self.odes.active == 3:
            x0 = np.array([x0,0])
        else:
            x0 = np.array([x0])

        # solve ode with numerical scheme        
        [t, x] = solver(ode, x0, h, timespan)
        [t_ref, x_ref] = ode_fun.ref_sol(ref, x0, timespan)

        # save data
        x = x[0,:] # only take first line of solutions
        x = x.tolist()
        t = t.tolist()
        x_ref = x_ref.tolist()
        t_ref = t_ref.tolist()
        self.source.data = dict(t=t, x=x)
        self.source_ref.data = dict(x_ref=x_ref, t_ref=t_ref)

        print "data was updated with parameters: h=" + str(h) + " and x0=" + str(x0)
