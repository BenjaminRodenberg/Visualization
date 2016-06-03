# Lagrange App
This app visualizes optimization under side conditions in 2D using Lagrange multipliers. The Isocontours of the objective function f(x,y) are plotted as well as the boundarycondition g(x,y)=0. A local minimum is acieved, if the gradients of f and g  are linearly dependent (i.e. parallel).
```
L = f+lambda*g
```
differentiation grad(L) yields
```
grad(f)=-lambda*grad(g)
g=0
```
## Running
This app can be run by typing
```
$ bokeh serve lagrange_app.py
```
into bash and then open
```
http://localhost:5006/lagrange_app
```
in the browser.

##ToDos
- [ ] generate running prototype