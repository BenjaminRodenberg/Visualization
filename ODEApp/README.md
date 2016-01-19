# ODE App
This app visualizes, how different ODE Solvers solve different ODEs. The user can interactively change stepwidth and starting value, as well as choose from 3 different solvers (explicit Euler, implicit Euler, implicit midpoint rule) and 2 different ODEs (Dahlquist test equation and logistic differential equation).

## Running
Enter 
```
$ bokeh-server --script run_app.py
```
in bash to run the app. Then enter
```
http://localhost:5006/bokeh/ode
```
in your browser to use the app in it.

##ToDos
- [x] Change structure of the App in the style of the sliders example
- [x] Improve GUI
- [x] Add oszillator ODE
- [x] publish this to the internet
- [x] Update to Bokeh 0.11
- [ ] Add störmer verlet (?) -> midpointrule might be sufficient...
- [ ] Add code for embedding.
