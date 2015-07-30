# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 22:04:14 2015

@author: benjamin
"""

import ODEFunctions as ODEfun;

import time

class ODEApp(object):   
    
    extra_generated_classes = [["FourierApp", "FourierApp", "VBox"]];
    
    T = 5;
    x0 = 1;
    h = 1;
    
    k=.5;
    G=.5;
    lam=-5;
    
    ODE = lambda self,t,x,x_0: ODEfun.dahlquist(t,x,x_0,self.lam);    
    #ODE = lambda self,t,x,x_0: ODEfun.logisticEquation(t,x,x_0,self.k,self.G);
    
    solverLibrary = [lambda f,x0,h,T: ODEfun.explEuler(f,x0,h,T),
                     lambda f,x0,h,T: ODEfun.implEuler(f,x0,h,T),
                     lambda f,x0,h,T: ODEfun.implMidpoint(f,x0,h,T)];
    
    solver = lambda self,f,x0,h,T: self.solverLibrary[0](f,x0,h,T);    
    
       
    def __init__(self):                
        from bokeh.document import Document
        from bokeh.session import Session
        from bokeh.models import ColumnDataSource 
        
        self.document = Document()
        self.session = Session()
        self.session.use_doc('ode')
        self.session.load_document(self.document)
        
        self.source = ColumnDataSource(data=dict(t=[], x=[], x_ref=[]))                
        
    def render(self):     
        self.init_curves();
        self.create_layout();
        self.document.add(self.layout);        
        self.init_solutions();
        
    def create_layout(self):
        """
        Initializes layout of the interactive bokeh plot
        """    
        from bokeh.models.widgets import VBox, Slider, VBoxForm, RadioButtonGroup        
        
        #slider controlling stepsize of the solver
        self.stepsize = Slider(
            title="stepsize", name='stepsize',
            value=self.h, start=0.1, end=1.0, step=.05
        );
        
        #slider controlling initial value of the ode
        self.startvalue = Slider(
            title="startvalue", name='startvalue',
            value=self.x0, start=-1, end=1, step=.1
        );
        
        #gives the opportunity to choose from different solvers
        self.solvers = RadioButtonGroup(
            labels=["ExplicitEuler", "ImplicitEuler", "MidpointRule"], active=0
        );
            
        self.stepsize.on_change('value', self,'input_change');
        self.startvalue.on_change('value', self,'input_change');
        self.solvers.on_change('active',self,'input_change');
        
        #lists all the controls in our plot
        self.controls = VBoxForm(
            children=[
                self.stepsize, self.startvalue, self.solvers
            ]
        )
        
        self.layout = VBox(self.controls,self.plot)   
        
    def init_curves(self):
        from bokeh.plotting import figure
        
        toolset = "crosshair,pan,reset,resize,wheel_zoom,box_zoom"       
        # Generate a figure container
        self.plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      title="fourier",#obj.text.value,
                      x_range=[0, self.T],
                      y_range=[-2.5, 2.5]
        )                     
        # Plot the line by the x,y values in the source property
        self.plot.line('t', 'x', source=self.source,
                  line_width=3,
                  line_alpha=0.6,
                  color='red'
        )
        self.plot.line('t','x_ref',source=self.source,
                  color='green',              
                  line_width=3,
                  line_alpha=0.6                  
        )        
        

    def input_change(self, obj, attrname, old, new):
        """Executes whenever the input form changes.

        It is responsible for updating the plot, or anything else you want.

        Args:
            obj : the object that changed
            attrname : the attr that changed
            old : old value of attr
            new : new value of attr
        """
        print "input changed!";
        self.update_data();        
        
    def init_solutions(self):
        """
        Called for initializing data of the plots.
        """        

        self.update_data();
        #important for getting data to the document        
        self.session.store_document(self.document)      
                
                
    def update_data(self):
        """Called each time that any watched property changes.

        This updates the sin wave data with the most recent values of the
        sliders. This is stored as two numpy arrays in a dict into the app's
        data source property.
        """
        
        # Get the current slider values
        self.h = self.stepsize.value;
        self.x0 = self.startvalue.value;  
        self.solver = self.solverLibrary[self.solvers.active];
        
        # solve ode with numerical scheme
        #[t,x,x_ref]=ODEfun.explEuler(lambda t,x,x0: ODEfun.dahlquist(t,x,x0,1),self.x0,self.h,self.T);
        [t,x,x_ref]=self.solver(self.ODE,self.x0,self.h,self.T);                

        x = x.tolist();
        t = t.tolist();
        x_ref = x_ref.tolist();

        self.source.data = dict( t = t , x = x , x_ref = x_ref) 
        
        #important for getting data to the document        
        self.session.store_document(self.document);
        
        print "data was updated with parameters: h="+str(self.h)+" and x0="+str(self.x0);
        
import bokeh.embed as embed  
appBokeh = ODEApp()
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
"""Bokeh server is now running the ODE app!"""
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
