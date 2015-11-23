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

from bokeh.models.widgets import VBox, Slider, RadioButtonGroup, VBoxForm, Dropdown, TextInput
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.plotting import figure

import numpy as np

import fourier_functions as ff
import fourier_tex as ft
import fourier_settings

class FourierApp(VBox):
    extra_generated_classes = [["FourierApp", "FourierApp", "VBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    function_type = Instance(RadioButtonGroup)
    degree = Instance(Slider)
    function_input = Instance(TextInput)

    # plot
    plot = Instance(Plot)

    # data
    source_fourier = Instance(ColumnDataSource)
    source_orig = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # initialize data source
        obj.source_fourier = ColumnDataSource(data=dict(t=[], x_fourier=[]))
        obj.source_orig = ColumnDataSource(data=dict(t=[], x_orig=[]))

        # initialize controls
        # slider controlling the base function
        obj.function_type = RadioButtonGroup(
            labels=fourier_settings.function_names, active=fourier_settings.function_init
        )

        # slider controlling degree of the fourier series
        obj.degree = Slider(
            title="degree", name='degree',
            value=fourier_settings.degree_init, start=fourier_settings.degree_min, end=fourier_settings.degree_max, step=fourier_settings.degree_step
        )

        obj.function_input = TextInput(value=fourier_settings.function_input_msg, title="my function:")

        # initialize plot
        toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      title="Fourier Series Approximation",
                      x_range=[fourier_settings.x_min, fourier_settings.x_max],
                      y_range=[fourier_settings.y_min, fourier_settings.y_max]
        )
        # Plot the line by the x,y values in the source property
        plot.line('t', 'x_orig', source=obj.source_orig,
                  line_width=3,
                  line_alpha=0.6,
                  color='red',
                  legend='original function'
        )
        plot.line('t','x_fourier',source=obj.source_fourier,
                  color='green',
                  line_width=3,
                  line_alpha=0.6,
                  legend='fourier series'
        )
        plot.patch([fourier_settings.timeinterval_start, fourier_settings.timeinterval_start,
                    fourier_settings.timeinterval_end,fourier_settings.timeinterval_end],
                   [-10**10,+10**10,+10**10,-10**10],
                   alpha = .2)
        obj.plot = plot

        # calculate data
        obj.update_data()

        # lists all the controls in our app
        obj.controls = VBoxForm(
            children=[
                obj.degree,
                obj.function_type,
                obj.function_input
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
        if not self.degree:
            return

        # event registration
        self.degree.on_change('value', self, 'input_change')
        self.function_input.on_change('value', self, 'input_change')
        self.function_type.on_change('active', self, 'type_input_change')

    def type_input_change(self, obj, attrname, old, new):
        if self.function_type.active == 3:
            self.function_input.value = fourier_settings.function_input_init
        else:
            self.function_input.value = fourier_settings.function_input_msg
            self.input_change(obj,attrname,old,new)


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
        TeX_string = self.update_data()  #update data and get new TeX
        self.send_request(TeX_string)   #send new TeX to server


    def update_data(self):
#==============================================================================
#         Called each time that any watched property changes.
#
#         This updates the fourier series expansion with the most recent values
#         of the slider. The new fourier series y data is stored as a numpy
#         arrays in a dict into the app's data source property.
#==============================================================================
        N = int(round(self.degree.value)) # Get the current slider values
        f_raw = fourier_settings.function_library[self.function_type.active]

        #function f(x) which will be approximated
        t = np.linspace(fourier_settings.x_min,fourier_settings.x_max,fourier_settings.resolution)
        x_orig = np.empty(len(t))

        if self.function_type.active == 3:
            fun_str = self.function_input.value
            f = f_raw(fun_str)
        else:
            self.function_input.value = fourier_settings.function_input_msg
            f = f_raw

        for i in range(len(t)):
            periodic_t = (t[i] - fourier_settings.timeinterval_start) \
                         % fourier_settings.timeinterval_length + \
                         fourier_settings.timeinterval_start
            x_orig[i] = f(periodic_t)


        # Generate Fourier series
        T = fourier_settings.timeinterval_length #length of one period of the function
        a,b = ff.coeff(f, fourier_settings.timeinterval_start, fourier_settings.timeinterval_end, N) #calculate coefficients
        x_fourier = np.empty(len(x_orig))

        for i in range(len(x_fourier)): # evaluate fourier series
            x_fourier[i] = ff.fourier_series(a,b,T,t[i])

        #saving data to plot
        self.source_orig.data = dict(t=t, x_orig=x_orig)
        self.source_fourier.data = dict(t=t,x_fourier=x_fourier)

        #generate new TeX string
        TeX_string = ft.generate_tex(a,b,T)

        print "data was updated with N = %d" % (N)

        return TeX_string


    def send_request(self,TeX_string):
#==============================================================================
#         Sends the TeX String via a request to the flask server. This directly
#         triggers the update of the html page.
#==============================================================================
        print "sending request..."
        #urllib.urlopen("http://localhost:5001/publish?TEX="+TeX_string)