# ODE App
This app visualizes, how different ODE Solvers solve different ODEs. The user can interactively change stepwidth and starting value, as well as choose from 3 different solvers (explicit Euler, implicit Euler, implicit midpoint rule) and 2 different ODEs (Dahlquist test equation and logistic differential equation).

## Running
Enter 
´´´
$ bokeh-server --script ODEApp.py
´´´
in bash to run the app. Then enter
´´´
http://localhost:5006/bokeh/ode
´´´
in your browser to use the app in it.

##ToDos
-[x] Change structure of the App in the style of the sliders example
-[ ] Improve GUI
-[ ] Add code for embedding, such that the app can be published on the internet.
