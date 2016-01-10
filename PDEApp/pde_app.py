# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

from __future__ import division

import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from bokeh.models.widgets import HBox, Slider, RadioButtonGroup, VBoxForm, TextInput
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.plotting import figure

import pde_settings


def parse(fun_str):
    from sympy import sympify, lambdify
    from sympy.abc import x

    fun_sym = sympify(fun_str)
    fun_lam = lambdify(x, fun_sym)
    return fun_lam


class PDEApp(HBox):
    # ==============================================================================
    # Only bokeh quantities for layout, data, controls... go here!
    # ==============================================================================
    extra_generated_classes = [["PDEApp", "PDEApp", "HBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    time = Instance(Slider)
    h = Instance(Slider)
    k = Instance(Slider)
    pde_type = Instance(RadioButtonGroup)
    solver_type = Instance(RadioButtonGroup)
    initial_condition = Instance(TextInput)

    # plot
    plot = Instance(Plot)

    # data
    plot_data = Instance(ColumnDataSource)
    mesh_data = Instance(ColumnDataSource)
    pde_specs = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # initialize data source
        obj.plot_data = ColumnDataSource(data=dict(x=[], u=[]))
        obj.mesh_data = ColumnDataSource(data=dict())
        obj.pde_specs = ColumnDataSource(data=dict(h=[], k=[]))

        # initialize controls
        # slider for going though time
        obj.time = Slider(
                title="time", name='time',
                value=pde_settings.t_init,
                start=pde_settings.t_min,
                end=pde_settings.t_max,
                step=pde_settings.t_step
        )
        # slider controlling spatial stepsize of the solver
        obj.h = Slider(title="spatial meshwidth", name='spatial meshwidth',
                       value=pde_settings.h_init,
                       start=pde_settings.h_min,
                       end=pde_settings.h_max,
                       step=pde_settings.h_step)
        # slider controlling spatial stepsize of the solver
        obj.k = Slider(title="temporal meshwidth", name='temporal meshwidth',
                       value=pde_settings.k_init,
                       start=pde_settings.k_min,
                       end=pde_settings.k_max,
                       step=pde_settings.k_step)
        # radiobuttons controlling pde type
        obj.pde_type = RadioButtonGroup(labels=['Heat', 'Wave'],
                                        active=0)
        # radiobuttons controlling solver type
        obj.solver_type = RadioButtonGroup(labels=['Explicit', 'Implicit'],
                                           active=0)
        # text input for IC
        obj.initial_condition = TextInput(value=pde_settings.IC_init,
                                          title="initial condition")

        # initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      # title=obj.text.value,
                      title="Time dependent PDEs",
                      x_range=[pde_settings.x_min, pde_settings.x_max],
                      y_range=[-1, 1]
                      )

        # Plot the numerical solution at time=t by the x,u values in the source property
        plot.line('x', 'u', source=obj.plot_data,
                  line_width=.5,
                  line_alpha=0.6,
                  line_dash=[4, 4],
                  color='red')
        plot.circle('x', 'u', source=obj.plot_data,
                    color='red',
                    legend='numerical solution')

        obj.plot = plot
        # calculate data
        obj.init_pde()

        # lists all the controls in our app
        obj.controls = VBoxForm(children=[obj.initial_condition,
                                          obj.time,
                                          obj.h,
                                          obj.k,
                                          HBox(children=[obj.pde_type, HBox(width=20), obj.solver_type],
                                               width=300)],
                                width=400)

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
        if not self.time:
            return

        # event registration
        self.time.on_change('value', self, 'time_change')
        self.h.on_change('value', self, 'mesh_change')
        self.k.on_change('value', self, 'mesh_change')
        self.solver_type.on_change('active', self, 'mesh_change')
        self.pde_type.on_change('active', self, 'mesh_change')
        self.initial_condition.on_change('value', self, 'mesh_change')

    def mesh_change(self, obj, attrname, old, new):
        h = self.h.value  # spatial meshwidth
        k = self.k.value  # temporal meshwidth
        solver_id = self.get_solver_id()  # solver
        print "mesh changed to " + str((h, k))
        print "using solver with id " + str(solver_id)
        self.update_mesh(h, k, solver_id)

    def get_solver_id(self):
        return self.pde_type.active * 2 + self.solver_type.active

    def time_change(self, obj, attrname, old, new):
        print str(obj.name) + " changed from " + str(old) + " to " + str(new)
        k = self.k.value
        t = self.time.value
        self.update_plot(k, t)
        print "new time: " + str(t)

    def init_pde(self):
        h = self.h.value
        k = self.k.value
        solver_id = self.get_solver_id()
        t = self.time.value

        self.update_mesh(h, k, solver_id)

    def update_mesh(self, h, k, solver_id):

        self.pde_specs.data = dict(h=[h], k=[k], solver_id=[solver_id])
        solver = pde_settings.solvers[solver_id]

        x0 = pde_settings.x_min
        x1 = pde_settings.x_max
        N = int(round((x1 - x0) / h + 1, 0))
        x = np.linspace(x0, x1, N)
        f0 = parse(self.initial_condition.value)
        u = np.empty(x.shape)
        for i in range(N):
            u[i] = f0(x[i])

        uold = np.array(u)  # this enforces neumann BC: u'(t=0)=0

        M = int(round(pde_settings.t_max / k, 0)) + 1

        mesh_dict = dict(x=x)

        for i in range(M):
            key = 'u' + str(i)
            mesh_dict[key] = u.tolist()
            unew = solver(uold, u, k, h)
            uold = u
            u = unew

        self.mesh_data.data = mesh_dict
        t = self.time.value
        self.update_plot(k, t)

    def update_plot(self, k, t):
        idx = int(round(t / k, 0))
        u_key = 'u' + str(idx)
        x = self.mesh_data.data['x']
        u = self.mesh_data.data[u_key]
        self.plot_data.data = dict(x=x, u=u)
