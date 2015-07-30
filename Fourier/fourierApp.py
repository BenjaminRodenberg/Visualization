#==============================================================================
# This file demonstrates a bokeh applet. The applet has been designed at TUM
# for educational purposes. The structure of the following code bases to large
# part on the work published on
# https://github.com/bokeh/bokeh/tree/master/examples/app/sliders_applet
#==============================================================================

import urllib, time
import numpy as np
import fourierFunctions as ff
import fourierTex as ft

class FourierApp(object):    
    extra_generated_classes = [["FourierApp", "FourierApp", "VBox"]]                
    start = 0; # start of plotting range
    end = 2*np.pi; # end of plotting range
    xRes = 200; #number of plotted points 
       
    def __init__(self):                
#==============================================================================
#         Initializes FourierApp object with all important properties
#==============================================================================
        from bokeh.document import Document
        from bokeh.session import Session
        from bokeh.models import ColumnDataSource 
        
        self.document = Document()
        self.session = Session()
        self.session.use_doc('fourier')
        self.session.load_document(self.document)
        #here the data is stored
        self.source = ColumnDataSource(data=dict(x=[], y=[], y_series=[]))                
        #finally renders the app
        self.render();
        
    def render(self):  
#==============================================================================
#         renders the App: Sets up layout, initializes plots...
#==============================================================================
        self.init_curves()        
        self.create_layout()    
        self.document.add(self.layout)
        self.init_data()
        
    def create_layout(self):
#==============================================================================
#         Initializes layout of the interactive bokeh plot        
#==============================================================================
        from bokeh.models.widgets import VBox, Slider, VBoxForm        
        
        #slider controlling degree of the fourier series
        self.degree = Slider(
            title="degree", name='degree',
            value=5.0, start=0, end=20.0, step=1
        )           
        #add behaviour to slider: slider change calls function input_change
        self.degree.on_change('value', self,'input_change')
        
        #lists all the controls in our plot
        self.controls = VBoxForm(
            children=[self.degree]);  
        #put plot and slider in a vertical box (VBox)
        self.layout = VBox(self.controls,self.plot);
        
    def init_curves(self):
#==============================================================================
#         Initializes the plots of our App.
#==============================================================================
        from bokeh.plotting import figure
        
        toolset = "crosshair,pan,reset,resize,save,wheel_zoom"       
        # Generate a figure container
        self.plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      title="fourier",#obj.text.value,
                      x_range=[0, 2*np.pi],
                      y_range=[-2.5, 2.5]
        )                     
        # Plot the line by the x,y values in the source property
        self.plot.line('x', 'y', source=self.source,
                  line_width=3,
                  line_alpha=0.6,
                  color='red'
        )
        self.plot.line('x','y_series',source=self.source,
                  color='green',              
                  line_width=3,
                  line_alpha=0.6                  
        )        
        

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
        TeX_string = self.update_data() #update data and get new TeX
        self.send_request(TeX_string)   #send new TeX to server
        
    def init_data(self):
#==============================================================================
#         Called for initializing data of the plots.        
#==============================================================================
        #function f(x) which will be approximated                
        x = np.linspace(self.start,self.end,self.xRes)
        y = np.empty(len(x))        
        for i in range(0,len(x)):
            y[i] = ff.f(x[i])

        #saving data to plot
        self.source.data = dict(x=x, y=y) 
        self.update_data();        
        self.session.store_document(self.document)
        
    def update_data(self):
#==============================================================================
#         Called each time that any watched property changes.
#
#         This updates the fourier series expansion with the most recent values
#         of the slider. The new fourier series y data is stored as a numpy 
#         arrays in a dict into the app's data source property.        
#==============================================================================
        x = self.source.data.get('x') # get data of f(x)
        y = self.source.data.get('y')        
        N = int(round((self.degree.value))) # Get the current slider values        
        
        # Generate Fourier series
        T = self.end - self.start #length of one period of the function
        a,b = ff.coeff(ff.f,self.start,self.end,N) #calculate coefficients
        y_series = np.empty(len(x))
        
        for i in range(0,len(x)): # evaluate fourier series           
            y_series[i] = ff.fourier_series(a,b,T,x[i])	

        #saving data to plot
        self.source.data = dict(x=x,y=y,y_series=y_series)         
        self.session.store_document(self.document)     
        
        #generate new TeX string
        TeX_string = ft.generate_tex(a,b,T)
        
        return TeX_string
    
    def send_request(self,TeX_string): 
#==============================================================================
#         Sends the TeX String via a request to the flask server. This directly
#         triggers the update of the html page.        
#==============================================================================        
        print "sending request..."
        urllib.urlopen("http://localhost:5001/publish?TEX="+TeX_string)
        
#==============================================================================
# main function
#==============================================================================
import bokeh.embed as embed  
appBokeh = FourierApp();

tag = embed.autoload_server(appBokeh.layout, appBokeh.session)
print("""\n use the following tag in your flask code: %s """ % tag)

link = appBokeh.session.object_link(appBokeh.document.context)
print("""You can also go to %s to see the plots on the Bokeh server directly""" 
% link)

print("""Bokeh server is now running the fourier app!""")

# saves the tag which identifies the app to a file, the Flask server later
# generates a html using this tag.
tag_f = open('current_tag.tmp', 'w')
tag_f.write(tag)
tag_f.close()

# run app.
try:
    while True:
        appBokeh.session.load_document(appBokeh.document)
        time.sleep(0.1)
except KeyboardInterrupt:
    print()
