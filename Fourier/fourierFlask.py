import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

from flask import Flask, Response, request

# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.iteritems() if k]
        
        return "%s\n\n" % "\n".join(lines)

appFlask = Flask(__name__)
subscriptions = []

# Client code consumes like this.
@appFlask.route("/")
def index():
    tag_f = open('current_tag','r')
    tag = tag_f.read()        
    
    debug_template = """
<!DOCTYPE html>
<html>
<head>
<title>Fourier Transform</title>

<script type="text/javascript"
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

</head>
<body>

<script>
  //
  //  Use a closure to hide the local variables from the
  //  global namespace
  //
  (function () {
    var QUEUE = MathJax.Hub.queue;  // shorthand for the queue
    var math = null, box = null;    // the element jax for the math output, and the box it's in

    //
    //  Hide and show the box (so it doesn't flicker as much)
    //
    var HIDEBOX = function () {box.style.visibility = "hidden"}
    var SHOWBOX = function () {box.style.visibility = "visible"}
    var i = 1;

    //
    //  Get the element jax when MathJax has produced it.
    //
    QUEUE.Push(function () {
      math = MathJax.Hub.getAllJax("MathOutput")[0];
      box = document.getElementById("box");
      i = i+1;
      SHOWBOX(); // box is initially hidden so the braces don't show
    });

    //
    //  The onchange event handler that typesets the math entered
    //  by the user.  Hide the box, then typeset, then show it again
    //  so we don't see a flash as the math is cleared and replaced.
    //    
    UpdateMath = function (TEX) {	
        console.log("running UpdateMath()");
        math.innerHTML = TEX;
        QUEUE.Push(HIDEBOX,["Text",math,TEX],SHOWBOX);
        console.log("updated TeX string!");
    }
    //
    // Flask server sent event handling
    //    
    var evtSrc = new EventSource("/subscribe");

    evtSrc.onmessage = function(e) {
        console.log("received Signal from Server:");        
        console.log(e.data);        
        UpdateMath(e.data);
    };

  })();
</script>

<div style="height:100px" onclick="UpdateMath()" class="box" id="box" style="visibility:hidden">
    <div id="MathOutput" class="output">\(     \)</div>
</div>

<p>
%s
</p>

</body>
</html>
""" % tag    
    return(debug_template)

@appFlask.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@appFlask.route("/publish")
def publish():
    TEX = request.args.get("TEX")    
    #Dummy data - pick up from request for real data
    def notify():        
        for sub in subscriptions[:]:
            sub.put(TEX)
    
    gevent.spawn(notify)
    
    return "OK"

@appFlask.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

if __name__ == "__main__":
    port=5001;
    print "Flask server is running!" 
    print "visit http://localhost:"+str(port)+" for using the app.\n"
    appFlask.debug = True
    server = WSGIServer(("", port), appFlask)
    server.serve_forever()   