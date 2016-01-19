# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging

logging.basicConfig(level=logging.DEBUG)

from mandel_par import mandel

from bokeh.models.widgets import HBox, Slider, RadioButtonGroup, VBoxForm, Dropdown, TextInput
from bokeh.models import Plot, ColumnDataSource, CustomJS
from bokeh.properties import Instance
from bokeh.plotting import figure

class MandelbrotApp(HBox):
    # ==============================================================================
    # Only bokeh quantities for layout, data, controls... go here!
    # ==============================================================================
    extra_generated_classes = [["MandelbrotApp", "MandelbrotApp", "HBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    focusx = Instance(Slider)
    focusy = Instance(Slider)
    width = Instance(Slider)
    dummy = Instance(Slider)

    # plot
    plot = Instance(Plot)

    # data
    source = Instance(ColumnDataSource)
    source_fig_specs = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # initialize data source
        obj.source = ColumnDataSource(data=dict(image=[],x0=[],y0=[],xw=[],yw=[]))
        obj.source_fig_specs = ColumnDataSource(data=dict(x0=[],y0=[],xw=[],yw=[]))

        # initialize controls
        # slider controlling x position of focus
        obj.focusx = Slider(
            title="x0", name='x0',
            value=-.5, start=-2.0, end=1.0, step=.01
        )
        # slider controlling y position of focus
        obj.focusy = Slider(
            title="y0", name='y0',
            value=0.0, start=-1.0, end=1.0, step=.01
        )
        # gives the opportunity to choose from different solvers
        obj.width = Slider(
            title="width", name='width',
            value=3.0, start=0.0, end=3.0, step=.01
        )

        obj.dummy = Slider(title="dummy", start=-2, end=2)

        # calculate data
        obj.update_data()

        # initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      x_range=[-2,1],
                      y_range=[-1.5,1.5],
                      tools=toolset,
                      title="Mandelbrot Set"
                      )
        # Plot the mandelbrot set
        plot.image(image='image',
                   x='x0',
                   y='y0',
                   dw='xw',
                   dh='yw',
                   palette="Spectral11",
                   source=obj.source)

        jscode = \
        """
        var data = source.get('data');
        var start = range.get('start');
        var end = range.get('end');
        data['%s'] = [start + (end - start) / 2];
        data['%s'] = [end - start];
        fun.trigger('value',0,(end-start)/2);
        source.trigger('change');
        """

        plot.x_range.callback = CustomJS(
                args=dict(source=obj.source_fig_specs, range=plot.x_range, fun=obj.dummy), code=jscode % ('x0', 'xw'))
        plot.y_range.callback = CustomJS(
                args=dict(source=obj.source_fig_specs, range=plot.y_range, fun=obj.dummy), code=jscode % ('y0', 'yw'))

        obj.plot = plot

        # lists all the controls in our app
        obj.controls = VBoxForm(
            children=[
                obj.focusy, obj.focusx, obj.width, obj.dummy
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
        if not self.focusx:
            return

        # event registration
        self.focusy.on_change('value', self, 'input_change')
        self.focusx.on_change('value', self, 'input_change')
        self.width.on_change('value', self, 'input_change')
        self.dummy.on_change('value',self, 'whine')


    def input_change(self, obj, attrname, old, new):
        # ==============================================================================
        # This function is called if input changes
        # ==============================================================================
        print "input changed!"
        self.update_data()


    def whine(self, obj, attrname, old, new):
        print "oh noooo i have to work :("


    def update_data(self):
        # ==============================================================================
        # Updated the data respective to input
        # ==============================================================================

        # default values for ODEs...
        focus_x = self.focusx.value
        focus_y = self.focusy.value
        w = self.width.value
        x0 = focus_x-w*.5
        y0 = focus_y-w*.5

        z = mandel(x0, y0, w, w, 400, 400, 1000)

        self.source.data = dict(image=[z.tolist()], x0=[x0], y0=[y0], yw=[w], xw=[w])

        print "data was updated."
        param = dict(x0=x0, y0=y0, w=w)
        print param
