# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 12:49:05 2015

@author: benjamin
"""

import boundaryVal_math as bv_math
import boundaryVal_helper as bv_help
import boundaryVal_settings as bv_settings

from bokeh.models.widgets import HBox, Slider, Button, VBoxForm
from bokeh.models import Plot,ColumnDataSource 
from bokeh.properties import Instance
from bokeh.plotting import figure


class BoundaryValApp(HBox):
        
    extra_generated_classes = [["BoundaryValApp", "BoundaryValApp", "HBox"]];    
    
    #data
    app_data = Instance(ColumnDataSource);    
    
    #layout
    controls = Instance(VBoxForm);    
    
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
        obj.app_data = ColumnDataSource(data=dict(alpha=[],alpha_left=[],alpha_right=[]));
        
        #initialize data
        obj.set_app_data(bv_settings.alpha,bv_settings.alpha_left,bv_settings.alpha_right);        

        #initialize controls        
        #slider controlling alpha of the the shooter
        obj.alphaSlider = Slider(
            title="Abschusswinkel", 
            name='alphaSlider',
            value=bv_settings.alpha, 
            start=bv_settings.alpha_min, 
            end=bv_settings.alpha_max, 
            step=bv_settings.alpha_step
        );           
        #buttons for shooting shorter or further
        obj.buttonFar = Button(
            label="steiler",type="default");
        obj.buttonShort = Button(
            label="flacher",type="default"); 

        #initialize plot
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"       
        # Generate a figure container
        plot = figure(title_text_font_size="12pt",
                      plot_height=200,
                      plot_width=400,
                      tools=toolset,
                      title="Schiessverfahren",#obj.text.value,
                      x_range=[-.5, 9.5],
                      y_range=[-.5, 4.5]
        )                     
        # Plot the line by the x,y values in the source property
        plot.line('rx', 'ry', source=obj.source,
                  line_width=3,
                  line_alpha=0.6,
                  color='red'
        )
        
        # insert picture of cannon and target                
        bv_help.drawTargetAt(plot,bv_settings.xTarget);        
        bv_help.drawCannon(plot);

        obj.plot = plot; 

        #calculate data
        obj.update_data();

        #lists all the controls in our app
        obj.controls = VBoxForm(
            children=[
                obj.alphaSlider,                
                obj.buttonShort,
                obj.buttonFar
            ]
        )
        
        #make layout        
        obj.children.append(obj.plot);####is this right?
        obj.children.append(obj.controls);  

        return obj                  
        
    def setup_events(self):
#==============================================================================
# Here we have to set up the event behaviour.        
#==============================================================================
        # recursively searches the right level?
        if not self.alphaSlider:
            return
            
        self.alphaSlider.on_change('value', self,'sliderChange');        
        self.buttonFar.on_click(self.shootFurther);
        self.buttonShort.on_click(self.shootShorter);    
        
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
        print "sliderChange(...) called...";  
        [alpha,alpha_left,alpha_right]=self.get_app_data();
        # Get the current slider values        
        alpha = self.alphaSlider.value; 
        print "new self.alpha = "+str(alpha)+".";
        self.set_app_data(alpha,alpha_left,alpha_right);
        self.update_data(); 
        print "sliderChange(...) exited!";  
    
    def shootFurther(self):
        print "shootFurther(...) called...";
        [alpha,alpha_left,alpha_right]=self.get_app_data();
        alpha_left = alpha;
        alpha = (alpha_left+alpha_right)/2;
        print "new self.alpha = "+str(alpha)+".";  
        self.set_app_data(alpha,alpha_left,alpha_right);
        self.update_data();
        print "shootFurther(...) exited!";        
        
    def shootShorter(self):
        print "shootShorter(...) called...";
        [alpha,alpha_left,alpha_right]=self.get_app_data();
        alpha_right = alpha;
        alpha = (alpha_left+alpha_right)/2;
        print "new self.alpha = "+str(alpha)+".";  
        self.set_app_data(alpha,alpha_left,alpha_right);    
        self.update_data();
        print "shootShorter(...) exited!";
        
    def get_app_data(self):
        alpha = self.app_data.data['alpha'][0];
        alpha_left = self.app_data.data['alpha_left'][0];
        alpha_right = self.app_data.data['alpha_right'][0];  
        print "getting app data:["+str(alpha)+","+str(alpha_left)+","+str(alpha_right)+"]";
        return alpha, alpha_left, alpha_right;
        
    def set_app_data(self,alpha,alpha_left,alpha_right): 
        print "setting app data to:["+str(alpha)+","+str(alpha_left)+","+str(alpha_right)+"]";
        self.app_data.data['alpha']=[alpha];
        self.app_data.data['alpha_left']=[alpha_left];
        self.app_data.data['alpha_right']=[alpha_right];        
        
    def update_data(self):
#==============================================================================
#         Called each time that any watched property changes.
#         This updates the shooting curve data with the most recent values of 
#         the sliders. This is stored as two numpy arrays in a dict into the
#         app's data source property.        
#==============================================================================
        print "update_data(...) called...";
        [alpha,alpha_left,alpha_right]=self.get_app_data();
        # solve shooting ODE with numerical scheme        
        print "computing new data...";
        [t,x]=bv_math.shootAlpha(alpha);
        print "new data computed.";

        rx = x[0,:];
        ry = x[1,:];        
        rx = rx.tolist();
        ry = ry.tolist();
        t = t.tolist();        
#==============================================================================
#         This section is not working! Problem with adding line to plot!
#==============================================================================
#==============================================================================
#         print "storing old try..."
#         oldrx = self.source.data['rx'];
#         oldry = self.source.data['ry'];                        
#         self.plot.line(oldrx,oldry,color='green')
#         print "old try stored."
#==============================================================================

        print "saving data..."
        self.source.data = dict( t = t , rx = rx , ry = ry);        
        print "data saved.";        
        print "data and plot was updated with parameters: alpha="+str(self.app_data.data['alpha'])+".";
        print "update_data(...) exited!";