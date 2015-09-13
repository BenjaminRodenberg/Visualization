# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 12:49:05 2015

@author: benjamin
"""

from boundaryValMath import *
from boundaryValHelper import *
import boundaryValSettings

import time

from bokeh.models.widgets import VBox,HBox, Slider, Button, VBoxForm, TextInput
from bokeh.models import Plot,ColumnDataSource 
from bokeh.properties import Instance
from bokeh.plotting import figure
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

class boundaryValApp(HBox):
        
    extra_generated_classes = [["BoundaryValApp", "BoundaryValApp", "HBox"]];    
    
    #layout
    controls = Instance(VBoxForm)    
    
    #controllable values    
    alphaSlider = Instance(Slider);
    buttonFar = Instance(Button);
    buttonShort = Instance(Button);    
    
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
        
        #initialize data source
        obj.source = ColumnDataSource(data=dict(rx=[], ry=[]));

        #initialize controls        
        #slider controlling alpha of the the shooter
        obj.alphaSlider = Slider(
            title="Abschusswinkel", 
            name='alphaSlider',
            value=self.alpha, 
            start=self.alpha_min, 
            end=self.alpha_max, 
            step=self.alpha_step
        );           
        #buttons for shooting shorter or further
        obj.buttonFar = Button(
            label="steiler",type="default");
        obj.buttonShort = Button(
            label="flacher",type="default"); 

        #initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"       
        # Generate a figure container
        obj.plot = figure(title_text_font_size="12pt",
                      plot_height=200,
                      plot_width=400,
                      tools=toolset,
                      title="Schiessverfahren",#obj.text.value,
                      x_range=[-.5, 9.5],
                      y_range=[-.5, 4.5]
        )                     
        # Plot the line by the x,y values in the source property
        obj.plot.line('rx', 'ry', source=obj.source,
                  line_width=3,
                  line_alpha=0.6,
                  color='red'
        )
        
        # insert picture of cannon and target                
        drawTargetAt(obj.plot,boundaryValSettings.xTarget);        
        drawCannon(obj.plot);

        obj.plot = plot;                             
        
    def render(self):     
        self.init_plot();
        self.create_layout();
        self.document.add(self.layout);        
        self.init_solution();
        
    def create_layout(self):
        """
        Initializes layout of the interactive bokeh plot
        """            
            
        self.alphaSlider.on_change('value', self,'sliderChange');        
        self.buttonFar.on_click(self.shootFurther);
        self.buttonShort.on_click(self.shootShorter);
        
        #lists all the controls in our plot
        self.controls = VBoxForm(
            children=[
                self.alphaSlider,                
                self.buttonShort,
                self.buttonFar
            ]
        )
        
        self.layout = VBox(self.plot,self.controls)     
    
    def init_solution(self):        
#==============================================================================
#         Called for initializing data of the plots.                
#==============================================================================
        print "init_solution(...) executed!";
        self.update_data();
        #important for getting data to the document        
        self.session.store_document(self.document);
        
    def sliderChange(self, obj, attrname, old, new):
#==============================================================================
#         Executes whenever the input form changes.
#         It is responsible for updating the plot, or anything else you want.
# 
#         Args:
#             obj : the object that changed
#             attrname : the attr that changed
#             old : old value of attr
#             new : new value of attr
#==============================================================================        
        print "sliderChange(...) executed!";
        # Get the current slider values
        self.alpha = self.alphaSlider.value; 
        print "new self.alpha = "+str(self.alpha)+".";
        self.update_data();  
    
    def shootFurther(self):
        print "shootFurther(...) executed!";
        self.alpha_left = self.alpha;
        self.alpha = (self.alpha_left+self.alpha_right)/2;
        print "new self.alpha = "+str(self.alpha)+".";
        #self.alphaSlider.value = self.alpha;        
        self.update_data();
        
        
    def shootShorter(self):
        print "shootShorter(...) executed!";
        self.alpha_right = self.alpha;        
        self.alpha = (self.alpha_left+self.alpha_right)/2;
        print "new self.alpha = "+str(self.alpha)+".";
        #self.alphaSlider.value = self.alpha;
        self.update_data();

    def update_data(self):
#==============================================================================
#         Called each time that any watched property changes.
#         This updates the shooting curve data with the most recent values of 
#         the sliders. This is stored as two numpy arrays in a dict into the
#         app's data source property.        
#==============================================================================
        print "update_data(...) executed!";
        
        # solve shooting ODE with numerical scheme        
        print "computing new data...";
        [t,x]=shootAlpha(self.alpha);
        print "new data computed.";

        rx = x[0,:];
        ry = x[1,:];        
        rx = rx.tolist();
        ry = ry.tolist();
        t = t.tolist();        
        
        print "storing old try..."
        oldrx = self.source.data['rx'];
        oldry = self.source.data['ry'];
        self.plot.line(oldrx,oldry,color='green')
        print "old try stored."
        

        print "saving data..."
        self.source.data = dict( t = t , rx = rx , ry = ry);        
        print "data saved.";
        
        #important for getting data to the document        
        print "storing document..."
        self.session.store_document(self.document);
        print "document stored."
        
        print "data and plot was updated with parameters: alpha="+str(self.alpha)+".";
        
import bokeh.embed as embed  
appBokeh = boundaryValApp()
appBokeh.render()

tag = embed.autoload_server(appBokeh.layout, appBokeh.session)
print(
"""\n use the following tag in your flask code: %s """ % tag
)

link = appBokeh.session.object_link(appBokeh.document.context)
print(
"""You can also go to %s to see the plots on the Bokeh server directly""" 
% link
)

print(
"""Bokeh server is now running the boundaryVal app!"""
)

tag_f = open('current_tag.tmp', 'w')
tag_f.write(tag)
tag_f.close()

try:
    while True:
        appBokeh.session.load_document(appBokeh.document)
        time.sleep(0.1)
except KeyboardInterrupt:
    print()        
        
        