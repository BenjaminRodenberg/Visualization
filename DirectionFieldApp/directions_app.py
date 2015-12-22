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

import quiver

import directions_settings, directions_helpers

class DirectionsApp(VBox):
    extra_generated_classes = [["DirectionsApp", "DirectionsApp", "VBox"]]

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    function_input = Instance(TextInput)

    # plot
    plot = Instance(Plot)

    # data
    source_segments = Instance(ColumnDataSource)
    source_patches = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # initialize data source
        obj.source_patches = ColumnDataSource(data=dict(xs=[], ys=[]))
        obj.source_segments = ColumnDataSource(data=dict(x0=[], y0=[], x1=[], y1=[]))

        # initialize controls
        # slider controlling the base function
        obj.function_input = TextInput(value=directions_settings.function_input_init, title="my function:")

        # initialize plot
        toolset = "crosshair,pan,reset,resize,save,wheel_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      title="Direction Field",
                      x_range=[directions_settings.x_min, directions_settings.x_max],
                      y_range=[directions_settings.y_min, directions_settings.y_max]
        )
        # Plot the direction field
        plot.segment('x0', 'y0', 'x1', 'y1', source=obj.source_segments)
        plot.patches('xs', 'ys', source=obj.source_patches)

        obj.plot = plot

        # calculate data
        obj.update_data()

        # lists all the controls in our app
        obj.controls = VBoxForm(
            children=[
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
        if not self.function_input:
            return

        # event registration
        self.function_input.on_change('value', self, 'input_change')

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
        self.update_data()  #update data

    def update_data(self):
        #==============================================================================
        #         Called each time that any watched property changes.
        #
        #         This updates the fourier series expansion with the most recent values
        #         of the slider. The new fourier series y data is stored as a numpy
        #         arrays in a dict into the app's data source property.
        #==============================================================================
        fun_str = self.function_input.value

        #function evaluated
        x, y, u, v, h = self.get_data(fun_str)

        #saving data to sources
        self.quiver_to_data(x, y, u, v, h)

        print "data was updated for f = %s" % (fun_str)

    def quiver_to_data(self, x, y, u, v, h):

        def quiver_to_segments(x, y, u, v, h):
            x = x.flatten()
            y = y.flatten()
            u = u.flatten()
            v = v.flatten()

            length = np.sqrt(u**2+v**2)
            u = u / length * h *.9
            v = v / length * h *.9

            x0 = x
            y0 = y
            x1 = x+u
            y1 = y+v

            return x0, y0, x1, y1

        def quiver_to_arrowheads(x, y, u, v, h):

            def __t_matrix(translate_x,translate_y):
                return np.array([[1, 0, translate_x],
                                 [0, 1, translate_y],
                                 [0, 0, 1]])

            def __r_matrix(rotation_angle):
                c = np.cos(rotation_angle)
                s = np.sin(rotation_angle)
                return np.array([[c, -s, 0],
                                 [s, +c, 0],
                                 [0, +0, 1]])

            def __head_template(x0, y0, u, v, type_id, headsize):
                if type_id is 0:
                    x_patch = 3 * [None]
                    y_patch = 3 * [None]

                    x1 = x0+u
                    x_patch[0] = x1
                    x_patch[1] = x1-headsize
                    x_patch[2] = x1-headsize

                    y1 = y0+v
                    y_patch[0] = y1
                    y_patch[1] = y1+headsize/np.sqrt(3)
                    y_patch[2] = y1-headsize/np.sqrt(3)
                elif type_id is 1:
                    x_patch = 4 * [None]
                    y_patch = 4 * [None]

                    x1 = x0+u
                    x_patch[0] = x1
                    x_patch[1] = x1-headsize
                    x_patch[2] = x1-headsize/2
                    x_patch[3] = x1-headsize

                    y1 = y0+v
                    y_patch[0] = y1
                    y_patch[1] = y1+headsize/np.sqrt(3)
                    y_patch[2] = y1
                    y_patch[3] = y1-headsize/np.sqrt(3)
                else:
                    raise Exception("unknown head type!")

                return x_patch, y_patch

            def __get_patch_data(x0, y0, u, v, headsize):

                angle = np.arctan(v/u)

                x_patch, y_patch = __head_template(x0, y0, u, v, type_id=1, headsize=headsize)

                T1 = __t_matrix(-x_patch[0], -y_patch[0])
                R = __r_matrix(angle)
                T2 = __t_matrix(x_patch[0], y_patch[0])
                T = T2.dot(R.dot(T1))

                for i in range(x_patch.__len__()):
                    v_in = np.array([x_patch[i],y_patch[i],1])
                    v_out = T.dot(v_in)
                    x_patch[i], y_patch[i], tmp = v_out

                return x_patch, y_patch

            x = x.flatten()
            y = y.flatten()
            u = u.flatten()
            v = v.flatten()

            length = np.sqrt(u**2+v**2)
            u = u / length * h *.9
            v = v / length * h *.9

            n_arrows = x.shape[0]
            xs = n_arrows * [None]
            ys = n_arrows * [None]

            headsize = .25 * h

            for i in range(n_arrows):
                print "(%d,%d)" % (x[i],y[i])
                x_patch, y_patch = __get_patch_data(x[i], y[i], u[i], v[i], headsize)
                xs[i] = x_patch
                ys[i] = y_patch

            return xs, ys

        x0, y0, x1, y1 = quiver_to_segments(x, y, u, v, h)
        ssdict = dict(x0=x0, y0=y0, x1=x1, y1=y1)
        print ssdict
        self.source_segments.data = ssdict

        xs, ys = quiver_to_arrowheads(x, y, u, v, h)
        spdict = dict(xs=xs, ys=ys)
        print spdict
        self.source_patches.data = spdict

    def get_data(self, fun_str):

        f = directions_helpers.parser(fun_str)
        h = directions_settings.resolution
        xx = np.arange(directions_settings.x_min, directions_settings.x_max, h)
        yy = np.arange(directions_settings.y_min, directions_settings.y_max, h)

        x, y = np.meshgrid(xx, yy)

        v = f(y)

        u = np.ones(v.shape)

        return x, y, u, v, h
