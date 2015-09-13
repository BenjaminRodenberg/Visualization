# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import logging

logging.basicConfig(level=logging.DEBUG)

import ODEFunctions as ODEfun;

from bokeh.models.widgets import VBox,HBox, Slider, RadioButtonGroup, VBoxForm, TextInput
from bokeh.models import Plot,ColumnDataSource 
from bokeh.properties import Instance
from bokeh.plotting import figure
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
import bokeh.embed as embed 

class ODEApp(HBox):   
#==============================================================================
# Only bokeh quantities for layout, data, controls... go here!
#==============================================================================
    extra_generated_classes = [["ODEApp", "ODEApp", "HBox"]];
    
    #layout
    controls = Instance(VBoxForm)    
    
    #controllable values    
    startvalue = Instance(Slider);
    stepsize = Instance(Slider);
    solvers = Instance(RadioButtonGroup);
    odes = Instance(RadioButtonGroup);
    
    #plot    
    plot = Instance(Plot);
    
    #data
    source = Instance(ColumnDataSource);
    
    @classmethod
    def create(cls):
#==============================================================================
# creates initial layout and data        
#==============================================================================
        obj = cls();
        
        #default values
        T = 5;
        x0 = 1;
        h = 1;        
        
        #initialize data source
        obj.source = ColumnDataSource(data=dict(t=[], x=[], x_ref=[]));

        #initialize controls        
        #slider controlling stepsize of the solver
        obj.stepsize = Slider(
            title="stepsize", name='stepsize',
            value=h, start=0.1, end=1.0, step=.05
        );        
        #slider controlling initial value of the ode
        obj.startvalue = Slider(
            title="startvalue", name='startvalue',
            value=x0, start=-1, end=1, step=.1
        );        
        #gives the opportunity to choose from different solvers
        obj.solvers = RadioButtonGroup(
            labels=["ExplicitEuler", "ImplicitEuler", "MidpointRule"], active=0
        );         
        #gives the opportunity to choose from different odes
        obj.odes = RadioButtonGroup(
            labels=["Dahlquist", "Logistic"], active=0
        );  

        #initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"       
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      #title=obj.text.value,
                      title="ODE",
                      x_range=[0, T],
                      y_range=[-2.5, 2.5]
        )          
        # Plot the numerical solution by the x,t values in the source property
        plot.line('t', 'x', source=obj.source,
                  line_width=3,
                  line_alpha=0.6,
                  color='red'
        )
        # Plot the analytical solution by the x_ref,t values in the source property
        plot.line('t','x_ref',source=obj.source,
                  color='green',              
                  line_width=3,
                  line_alpha=0.6                  
        )        
        obj.plot = plot;
        #calculate data
        obj.update_data();
        
        #lists all the controls in our app
        obj.controls = VBoxForm(
            children=[                
                obj.stepsize, obj.startvalue, obj.solvers, obj.odes
            ]
        )
        
        #make layout
        obj.children.append(obj.controls);        
        obj.children.append(obj.plot);  
        
        #don't forget to return!
        return obj
        
    def setup_events(self):
#==============================================================================
# Here we have to set up the event behaviour.        
#==============================================================================
        # recursively searches the right level?
        if not self.startvalue:
            return
                        
        # event registration
        self.stepsize.on_change('value', self,'input_change');
        self.startvalue.on_change('value', self,'input_change');
        self.solvers.on_change('active',self,'input_change');     
        self.odes.on_change('active',self,'input_change');  
                                   
    def input_change(self, obj, attrname, old, new):
#==============================================================================
# This function is called if input changes
#==============================================================================
        print "input changed!";
        self.update_data();                              
                
    def update_data(self):
#==============================================================================
# Updated the data respective to input
#==============================================================================
        
        #default values for ODEs...
        k=5;
        G=.5;
        lam=-5;    
        T=5;
        #available ODEs
        ODELibrary = [lambda t,x,x_0: ODEfun.dahlquist(t,x,x_0,lam),
                      lambda t,x,x_0: ODEfun.logisticEquation(t,x,x_0,k,G)];
        #available solvers
        solverLibrary = [lambda f,x0,h,T: ODEfun.explEuler(f,x0,h,T),
                         lambda f,x0,h,T: ODEfun.implEuler(f,x0,h,T),
                         lambda f,x0,h,T: ODEfun.implMidpoint(f,x0,h,T)];                
        
        # Get the current slider values
        h = self.stepsize.value;
        x0 = self.startvalue.value;  
        solver = solverLibrary[self.solvers.active];
        ODE = ODELibrary[self.odes.active];
        
        # solve ode with numerical scheme        
        [t,x,x_ref]=solver(ODE,x0,h,T);                

        # save data
        x = x.tolist();
        t = t.tolist();
        x_ref = x_ref.tolist();
        self.source.data = dict( t = t , x = x , x_ref = x_ref) 
                
        print "data was updated with parameters: h="+str(h)+" and x0="+str(x0);
        
@bokeh_app.route("/bokeh/ode/")
@object_page("ode")
def make_ode_app():
    app = ODEApp.create()     
    return app
