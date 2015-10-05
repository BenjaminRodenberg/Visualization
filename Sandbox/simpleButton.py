from bokeh.models.widgets import HBox, Button, VBoxForm
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page

class ButtonApp(HBox):  
    extra_generated_classes = [["ButtonApp", "ButtonApp", "HBox"]];    
    button = Instance(Button);
    controls = Instance(VBoxForm);
    
    @classmethod
    def create(cls):
        print "creating app..."        
        obj = cls();
        obj.button = Button(label="Foo", type="success");
        obj.button.label = "Bar";
        obj.controls = VBoxForm(
            children=[
                obj.button
            ]
        )                
        obj.children.append(obj.controls);          
        print "created app!"
        return obj;

    def setup_events(self):
        # recursively searches the right level?
        if not self.button:
            return
        self.button.on_click(self.changeLabel);        
        
    def changeLabel(self):
        print "changing label..."
        self.button.label="BarBar";	
        print "changed label!"
        
@bokeh_app.route("/bokeh/simpleButton/")
@object_page("simpleButton")
def make_ode():
    app = ButtonApp.create()     
    return app         


