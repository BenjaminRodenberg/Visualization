# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 12:49:05 2015

@author: benjamin
"""

import boundaryVal_math as bv_math
import boundaryVal_helper as bv_help
import boundaryVal_settings as bv_settings

from bokeh.models.widgets import VBox, Slider, RadioButtonGroup, VBoxForm
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.plotting import figure

import numpy as np


class BoundaryValApp(VBox):
    extra_generated_classes = [["BoundaryValApp", "BoundaryValApp", "VBox"]]

    # data
    app_data = Instance(ColumnDataSource)

    # layout
    controls = Instance(VBoxForm)

    # controllable values
    # alphaSlider = Instance(Slider)
    buttonShortSameFar = Instance(RadioButtonGroup)

    # plot
    plot = Instance(Plot)

    # data
    source = Instance(ColumnDataSource)
    source_short = Instance(ColumnDataSource)
    source_far = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        # ==============================================================================
        # creates initial layout and data
        # ==============================================================================
        obj = cls()

        # initialize data source
        obj.source = ColumnDataSource(data=dict(rx=[],
                                                ry=[]))
        obj.source_short = ColumnDataSource(data=dict(rx_short=[],
                                                      ry_short=[]))
        obj.source_far = ColumnDataSource(data=dict(rx_far=[],
                                                    ry_far=[]))
        obj.app_data = ColumnDataSource(data=dict(alpha=[bv_settings.alpha_init],
                                                  alpha_left=[bv_settings.alpha_left],
                                                  alpha_right=[bv_settings.alpha_right]))

        # initialize controls
        # slider controlling alpha of the the shooter
        # obj.alphaSlider = Slider(title="Abschusswinkel",
        #                          name='alphaSlider',
        #                          value=bv_settings.alpha_init,
        #                          start=bv_settings.alpha_min,
        #                          end=bv_settings.alpha_max,
        #                          step=bv_settings.alpha_step
        #                          )
        # buttons for shooting shorter or further
        obj.buttonShortSameFar = RadioButtonGroup(labels=bv_settings.button_labels,
                                                  active=bv_settings.button_init)

        # initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=bv_settings.fig_height,
                      plot_width=bv_settings.fig_width,
                      tools=toolset,
                      title=bv_settings.title,  # obj.text.value,
                      x_range=[bv_settings.min_x, bv_settings.max_x],
                      y_range=[bv_settings.min_y, bv_settings.max_y]
                      )
        # Plot the line by the x,y values in the source property
        plot.line('rx', 'ry',
                  source=obj.source,
                  line_width=3,
                  line_alpha=0.6,
                  color='blue',
                  legend='current shot')
        plot.line('rx_short', 'ry_short',
                  source=obj.source_short,
                  line_width=1,
                  line_alpha=.6,
                  line_dash=[4, 4],
                  color='green',
                  legend='old next shorter shot')
        plot.line('rx_far', 'ry_far',
                  source=obj.source_far,
                  line_width=1,
                  line_alpha=.6,
                  line_dash=[4, 4],
                  color='red',
                  legend='old next farther sh')

        # insert picture of cannon and target                
        bv_help.drawTargetAt(plot, np.random.rand()*10)
        bv_help.drawCannon(plot)

        obj.plot = plot

        # calculate data
        obj.update_data()

        # lists all the controls in our app
        obj.controls = VBoxForm(children=[#obj.alphaSlider,
                                          obj.buttonShortSameFar])

        # make layout
        obj.children.append(obj.plot)
        obj.children.append(obj.controls)

        return obj

    def setup_events(self):
        # ==============================================================================
        # Here we have to set up the event behaviour.
        # ==============================================================================
        # recursively searches the right level?
        if not self.buttonShortSameFar:
            return

        #self.alphaSlider.on_change('value', self, 'sliderChange')
        self.buttonShortSameFar.on_change('active', self, 'shootChange')

    def sliderChange(self, obj, attrname, old, new):
        # ==============================================================================
        #         Executes whenever the input form changes.
        #         It is responsible for updating the plot, or anything else you want.
        #
        #         Args:
        #             obj : the object that changed
        #             attrname : the attr that changed
        #             old : old value of attr
        #             new : new value of attr
        # ==============================================================================
        print "sliderChange(...) called..."
        # Get the current slider values
        self.app_data.data = dict(alpha=[self.alphaSlider.value],
                                  alpha_left=self.app_data.data['alpha_left'],
                                  alpha_right=self.app_data.data['alpha_right'])
        print "new self.alpha = " + str(self.app_data.data['alpha'][0]) + "."
        self.update_data()
        print "sliderChange(...) exited!"

    def shootChange(self, obj, attrname, old, new):
        print "shootChange(...) called..."
        if self.buttonShortSameFar.active is 1:
            print "doing nothing!"
            print "shootChange(...) exited!"
            return
        if self.buttonShortSameFar.active is 0:
            print "shoot shorter!"
            self.shootShorter()
        elif self.buttonShortSameFar.active is 2:
            print "shoot further!"
            self.shootFurther()
        else:
            print "unknown shooting!"

        print "new alpha = %d " % self.app_data.data['alpha'][0]
        print "new alpha_left = %d " % self.app_data.data['alpha_left'][0]
        print "new alpha_right = %d " % self.app_data.data['alpha_right'][0]
        self.buttonShortSameFar.active = 1
        self.buttonShortSameFar.labels[1] = str(self.app_data.data['alpha'][0])
        print "shootChange(...) exited!"

    def shootFurther(self):
        print "shootFurther(...) called..."
        print "old alpha = %d " % self.app_data.data['alpha'][0]
        print "old alpha_left = %d " % self.app_data.data['alpha_left'][0]
        print "old alpha_right = %d " % self.app_data.data['alpha_right'][0]

        alpha_right = self.app_data.data['alpha_right'][0]
        alpha_left = self.app_data.data['alpha'][0]
        self.app_data.data = dict(alpha=[(alpha_left + alpha_right) / 2],
                                  alpha_left=[alpha_left],
                                  alpha_right=[alpha_right])
        print "new self.alpha = " + str(self.app_data.data['alpha'][0]) + "."
        self.update_data()
        print "shootFurther(...) exited!"

    def shootShorter(self):
        print "shootShorter(...) called..."
        print "old alpha = %d " % self.app_data.data['alpha'][0]
        print "old alpha_left = %d " % self.app_data.data['alpha_left'][0]
        print "old alpha_right = %d " % self.app_data.data['alpha_right'][0]
        alpha_right = self.app_data.data['alpha'][0]
        alpha_left = self.app_data.data['alpha_left'][0]
        self.app_data.data = dict(alpha=[(alpha_left + alpha_right) / 2],
                                  alpha_left=[alpha_left],
                                  alpha_right=[alpha_right])
        print "new self.alpha = " + str(self.app_data.data['alpha'][0]) + "."
        self.update_data()
        print "shootShorter(...) exited!"

    def update_data(self):
        # ==============================================================================
        #         Called each time that any watched property changes.
        #         This updates the shooting curve data with the most recent values of
        #         the sliders. This is stored as two numpy arrays in a dict into the
        #         app's data source property.
        # ==============================================================================
        print "update_data(...) called..."
        # solve shooting ODE with numerical scheme        
        print "computing new data..."
        [t, x] = bv_math.shootAlpha(self.app_data.data['alpha'][0])
        [t_short, x_short] = bv_math.shootAlpha(self.app_data.data['alpha_left'][0])
        [t_far, x_far] = bv_math.shootAlpha(self.app_data.data['alpha_right'][0])
        print "new data computed."

        self.buttonShortSameFar.labels[1] = str(self.app_data.data['alpha'][0])

        rx = x[0, :]
        ry = x[1, :]
        rx = rx.tolist()
        ry = ry.tolist()
        rx_short = x_short[0, :]
        ry_short = x_short[1, :]
        rx_short = rx_short.tolist()
        ry_short = ry_short.tolist()
        rx_far = x_far[0, :]
        ry_far = x_far[1, :]
        rx_far = rx_far.tolist()
        ry_far = ry_far.tolist()
        # ==============================================================================
        #         This section is not working! Problem with adding line to plot!
        # ==============================================================================
        # ==============================================================================
        #         print "storing old try..."
        #         oldrx = self.source.data['rx'];
        #         oldry = self.source.data['ry'];
        #         self.plot.line(oldrx,oldry,color='green')
        #         print "old try stored."
        # ==============================================================================

        print "saving data..."
        self.source.data = dict(rx=rx, ry=ry)
        self.source_short.data = dict(rx_short=rx_short, ry_short=ry_short)
        self.source_far.data = dict(rx_far=rx_far, ry_far=ry_far)
        print "data saved."
        print "data and plot was updated with parameters: alpha=" + str(self.app_data.data['alpha']) + "."
        print "update_data(...) exited!"
