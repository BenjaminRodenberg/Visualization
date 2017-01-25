__author__ = 'benjamin'

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import HBox, Slider, RadioButtonGroup, VBoxForm, Dropdown
from bokeh.models import Plot, ColumnDataSource, Int, List, HasProps
from bokeh.properties import Instance
from bokeh.plotting import figure

import numpy as np

class ObjA(HasProps):
    calls = Int

class MinApp(HBox):
    # ==============================================================================
    # Only bokeh quantities for layout, data, controls... go here!
    # ==============================================================================
    extra_generated_classes = [["MinApp", "MinApp", "HBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    slope = Instance(Slider)

    # plot
    plot = Instance(Plot)

    # data
    source = Instance(ColumnDataSource)

    myObj = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # default values
        m = 1

        obj.myObj = ColumnDataSource(data=dict(someObjects=[ObjA(calls=0)]))

        # initialize data source
        obj.source = ColumnDataSource(data=dict(x=[], y=[]))

        # initialize controls
        # slider controlling stepsize of the solver
        obj.slope = Slider(
            title="slope", name='slope',
            value=m, start=-1, end=1, step=.05
        )

        # initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      # title=obj.text.value,
                      title="line",
                      x_range=[0, 1],
                      y_range=[-1, 1]
                      )
        # Plot the numerical solution by the x,t values in the source property
        plot.line('x', 'y', source=obj.source)
        obj.plot = plot

        # calculate data
        #obj.update_data()

        # lists all the controls in our app
        obj.controls = VBoxForm(
            children=[
                obj.slope
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
        if not self.slope:
            return

        # event registration
        self.slope.on_change('value', self, 'input_change')

    def input_change(self, obj, attrname, old, new):
        # ==============================================================================
        # This function is called if input changes
        # ==============================================================================
        print "input changed!"
        print "calls before this call: "+str(self.myObj.data)
        self.update_data()
        print "calls after this call: "+str(self.myObj.data)

    def update_data(self):
        # ==============================================================================
        # Updated the data respective to input
        # ==============================================================================

        theObj = self.myObj.data['someObjects'][0]
        print theObj
        calls = theObj.calls
        calls += 1
        newObj = ObjA(calls = 1)
        self.myObj.data = dict(someObjects = [newObj])

        x = np.linspace(0,1)
        y = np.empty(x.shape)
        n = x.size
        m = self.slope.value
        t = 0



        for i in range(n):
            y[i] = m*x[i]+t

        x=x.tolist()
        y=y.tolist()

        self.source.data = dict(x=x, y=y)

        print "data was updated with parameters: m=" + str(m)