# ODE App
This app visualizes, how different ODE Solvers solve different ODEs. The user can interactively change stepwidth and starting value, as well as choose from 3 different solvers (explicit Euler, implicit Euler, implicit midpoint rule) and 2 different ODEs (Dahlquist test equation and logistic differential equation).

## Running
This app can be run by typing
```
$ bokeh serve ode_app.py
```
into bash and then open
```
http://localhost:5006/ode_app
```
in the browser.

##ToDos
- [x] Change structure of the App in the style of the sliders example
- [x] Improve GUI
- [x] Add oszillator ODE
- [x] publish this to the internet
- [x] Update to Bokeh 0.11
- [ ] add support for dynamic user view update
- [ ] Add quiver field to ode app?
- [ ] proper documentation
- [ ] Add code for embedding.
