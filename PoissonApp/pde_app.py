# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging

logging.basicConfig(level=logging.DEBUG)

import numpy as np

from bokeh.models.widgets import HBox, Slider, RadioButtonGroup, VBoxForm, Dropdown
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance, Color
from bokeh.plotting import figure
from bokeh.models.mappers import LinearColorMapper

from pde_settings import svg_palette_jet

class PDEApp(HBox):
    # ==============================================================================
    # Only bokeh quantities for layout, data, controls... go here!
    # ==============================================================================
    extra_generated_classes = [["PDEApp", "PDEApp", "HBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    value1 = Instance(Slider)
    value2 = Instance(Slider)

    # plot
    plot = Instance(Plot)

    # data
    source = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # initialize data source
        obj.source = ColumnDataSource(data=dict(z=[]))

        # initialize controls
        # slider controlling stepsize of the solver
        obj.value2 = Slider(
                title="value2", name='value2',
                value=1, start=-1, end=+1, step=.1
        )
        # slider controlling initial value of the ode
        obj.value1 = Slider(
                title="value1", name='value1',
                value=0, start=-1, end=+1, step=.1
        )

        # initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      # title=obj.text.value,
                      title="somestuff",
                      x_range=[-1, 1],
                      y_range=[-1, 1]
                      )
        # Plot the numerical solution by the x,t values in the source property

        plot.image(image='z',
                   x=-1, y=-1, dw=2, dh=2,
                   #palette="Spectral11",
                   color_mapper = LinearColorMapper(palette=svg_palette_jet,low=-2,high=2),
                   source=obj.source
                   )

        obj.plot = plot
        # calculate data
        obj.update_data()

        # lists all the controls in our app
        obj.controls = VBoxForm(
                children=[
                    obj.value1, obj.value2
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
        if not self.value1:
            return

        # event registration
        self.value2.on_change('value', self, 'input_change')
        self.value1.on_change('value', self, 'input_change')

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
        print "updating data..."
        v1 = self.value1.value
        v2 = self.value2.value

        N = 200
        x,y = np.meshgrid(np.linspace(-1,1,N),np.linspace(-1,1,N))
        z = v1*x**2 + v2*y**2

        self.source.data = dict(z=[z.tolist()])

        print "data was updated with parameters: v1=" + str(v1) + " and v2=" + str(v2)
        print "new z:"
        print z
