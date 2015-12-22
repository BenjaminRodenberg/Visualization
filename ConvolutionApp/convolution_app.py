# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""
#==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples
#==============================================================================

import logging

logging.basicConfig(level=logging.DEBUG)

from bokeh.models.widgets import VBox, Slider, RadioButtonGroup, VBoxForm, HBox, Dropdown, TextInput
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance, Bool
from bokeh.plotting import figure

from scipy.integrate import quad

import numpy as np

import convolution_settings

import convolution_functions as cf

class ConvolutionApp(VBox):
    extra_generated_classes = [["ConvolutionApp", "ConvolutionApp", "VBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    x_value = Instance(Slider)
    function_type = Instance(RadioButtonGroup)
    function1_input = Instance(TextInput)
    function2_input = Instance(TextInput)

    # plot
    plot = Instance(Plot)

    # data
    source_function1 = Instance(ColumnDataSource)
    source_function2 = Instance(ColumnDataSource)
    source_result = Instance(ColumnDataSource)
    source_convolution = Instance(ColumnDataSource)
    source_xmarker = Instance(ColumnDataSource)
    source_overlay = Instance(ColumnDataSource)

    # primitive properties
    update_is_enabled = Bool

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # initialize data source
        obj.source_function1 = ColumnDataSource(data=dict(x=[], y=[]))
        obj.source_function2 = ColumnDataSource(data=dict(x=[], y=[]))
        obj.source_result = ColumnDataSource(data=dict(x=[], y=[]))
        obj.source_convolution = ColumnDataSource(data=dict(x=[], y=[]))
        obj.source_xmarker = ColumnDataSource(data=dict(x=[], y=[]))
        obj.source_overlay = ColumnDataSource(data=dict(x=[], y=[]))

        # initialize properties
        obj.update_is_enabled = True

        # initialize controls
        # slider controlling the base function
        obj.function_type = RadioButtonGroup(
            labels=convolution_settings.function_names, active=convolution_settings.function_init
        )

        # slider controlling degree of the fourier series
        obj.x_value = Slider(
            title="x value", name='x value',
            value=convolution_settings.x_value_init,
            start=convolution_settings.x_value_min, end=convolution_settings.x_value_max,
            step=convolution_settings.x_value_step
        )

        obj.function1_input = TextInput(
            value=convolution_settings.function1_input_msg,
            title="my first function:"
        )

        obj.function2_input = TextInput(
            value=convolution_settings.function2_input_msg,
            title="my second function:"
        )

        # initialize plot
        toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      title="Fourier Series Approximation",
                      x_range=[convolution_settings.x_min_view, convolution_settings.x_max_view],
                      y_range=[convolution_settings.y_min_view, convolution_settings.y_max_view]
        )
        # Plot the line by the x,y values in the source property
        plot.line('x', 'y', source=obj.source_function1,
                  line_width=3,
                  line_alpha=0.6,
                  color='red',
                  legend='f1'
        )
        plot.line('x','y',source=obj.source_function2,
                  color='green',
                  line_width=3,
                  line_alpha=0.6,
                  legend='f2'
        )
        plot.line('x','y',source=obj.source_result,
                  color='blue',
                  line_width=3,
                  line_alpha=0.6,
                  legend='f1*f2'
        )
        plot.scatter('x','y',source=obj.source_xmarker,
                     color='black'
        )
        plot.line('x','y',source=obj.source_xmarker,
                  color='black',
                  line_width=3)
        plot.patch('x','y_pos',source=obj.source_overlay,
                   fill_color='blue',
                   fill_alpha = .2)
        plot.patch('x','y_neg',source=obj.source_overlay,
                   fill_color='red',
                   fill_alpha = .2)


        obj.plot = plot

        # calculate data
        obj.update_data()

        # lists all the controls in our app
        obj.controls = VBoxForm(
            children=[
                obj.x_value,
                obj.function_type,
                HBox(children=[obj.function1_input, obj.function2_input])
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
        if not self.x_value:
            return

        # event registration
        self.x_value.on_change('value', self, 'x_input_change')
        self.function1_input.on_change('value', self, 'input_change')
        self.function2_input.on_change('value', self, 'input_change')
        self.function_type.on_change('active', self, 'type_input_change')

    def type_input_change(self, obj, attrname, old, new):
        print "changed function type from "+str(old)+" to "+str(new)

        if self.function_type.active == convolution_settings.default_function_id:
            self.update_is_enabled = False
            self.function1_input.value = convolution_settings.function1_input_init
            self.function2_input.value = convolution_settings.function2_input_init
            self.update_is_enabled = True
        else:
            self.update_is_enabled = False
            self.function1_input.value = convolution_settings.function1_input_msg
            self.function2_input.value = convolution_settings.function2_input_msg
            self.update_is_enabled = True

        self.input_change(obj, attrname, old, new)

    def x_input_change(self, obj, attrname, old, new):
        print "changed x value from "+str(old)+" to "+str(new)
        self.input_change(obj, attrname, old, new)

    def input_change(self, obj, attrname, old, new):
#==============================================================================
#         Executes whenever the input form changes.
#         It is responsible for updating the plot, or anything else you want.
#         Args:
#             obj : the object that changed
#             attrname : the attr that changed
#             old : old value of attr
#             new : new value of attr
#==============================================================================
        if self.update_is_enabled:
            print "updating data..."
            self.update_data()  #update data and get new TeX
            print "done!"
        else:
            print "updating data prohibited."


    def update_data(self):
#==============================================================================
#         Called each time that any watched property changes.
#
#         This updates the fourier series expansion with the most recent values
#         of the slider. The new fourier series y data is stored as a numpy
#         arrays in a dict into the app's data source property.
#==============================================================================
        x_value = self.x_value.value # Get the current slider values
        f_raw = convolution_settings.function_library[self.function_type.active]

        #function f(x) which will be approximated
        x = np.linspace(convolution_settings.x_min,convolution_settings.x_max,convolution_settings.resolution)
        y1 = np.empty(x.size)
        y2 = np.empty(x.size)
        y2shift = np.empty(x.size)

        width = convolution_settings.x_max - convolution_settings.x_min
        h = float(width) / float(convolution_settings.resolution)

        if self.function_type.active == convolution_settings.default_function_id:
            print "behaviour for custom user function "
            fun1_str = self.function1_input.value
            fun2_str = self.function2_input.value
            print "given strings:"
            print "\tfirst function:\t"+fun1_str
            print "\tsecond function:\t"+fun2_str
            f1 = f_raw(fun1_str,h)
            f2 = f_raw(fun2_str,h)
            print "functions used:"
            print "\tfirst function:\t"+str(f1)
            print "\tsecond function:\t"+str(f2)
        else:
            print "behaviour for predefined function"
            f1 = f_raw
            f2 = f_raw
            print "functions used:"
            print "\tfirst function:\t"+str(f1)
            print "\tsecond function:\t"+str(f2)

        y1 = f1(x)
        y2 = f2(x)
        y2shift = f2(x_value-x)
        y3 = np.convolve(y1,y2,mode='same')/x.size*width

        y_positive, y_negative = cf.compute_overlay_vector(y1,y2shift)

        #saving data to plot
        self.source_overlay.data = dict(x=np.concatenate([x,x[-1::-1]]), y_pos=y_positive, y_neg=y_negative)
        self.source_function1.data = dict(x=x, y=y1)
        self.source_function2.data = dict(x=x, y=y2shift)
        self.source_result.data = dict(x=x, y=y3)

        y_value = cf.find_value(x, y3, x_value)
        self.source_xmarker.data = dict(x=[x_value,x_value], y=[y_value,0])
