# ODESystemsApp
Plots direction field for arbitrary functions (u(x,y) and v(x,y)) and critical points. Additionally plots streamline for 
initial value (x0,y0).

## Running
Enter 
```
$ bokeh-server --script run_app.py
```
in bash to run the app. Then enter
```
http://localhost:5006/bokeh/odesystem
```
in your browser to use the app in it.

##ToDos
- [x] Add streamlines
- [x] Add support for plotting of critical points
- [x] Add support for plotting of critical lines
- [x] publish this to the internet
- [x] Update to Bokeh 0.11
- [ ] Add standard examples as predefined equations (circular attractor...)
- [ ] Improve GUI with panels
- [ ] Try to improve speed
- [ ] Add code for embedding.
