# Visualization
Webbased visualization for math content via Bokeh
This Repository contains different prototypes for WebApps for the visualization of math content for lectures at TUM (Technische Universität München).

## Running
### Local
For running all the complete apps type
```
bokeh serve filename.py
```
and navigate to the respective site

### Internet
For publishing all apps to the internet run the same command with the option
```
--host <globalip>:5006
```
for accepting connections to the server.

## ToDos
### Update to version 11
- [x] Update all Apps to version 11
    - [x] BoundaryValApp
    - [x] ODEApp
    - [x] FourierApp
    - [x] ODESystemApp
    - [x] PDEApp
    - [x] ConvolutionApp
    - [x] MandelbrotApp
- [x] Find out, what changes w.r.t. publishing content
- [x] Update README files instruction for running
- [ ] Merge with master

### On particular Apps
- [x] Find out how to bring an app to the internet ( see [Gallery](http://bokeh.pydata.org/en/latest/docs/gallery.html) ). How to get from an app like [Examples/Stocks](https://github.com/BenjaminRueth/Visualization/tree/master/Examples/ExampleStocks) to an app running in the internet?
- [x] Finalize [BoundaryValApp](https://github.com/BenjaminRueth/Visualization/tree/master/BoundaryValApp)
- [x] Finalize [ODEApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODEApp)
- [x] Finalize [FourierApp](https://github.com/BenjaminRueth/Visualization/tree/master/FourierApp)
- [ ] Finalize [ODESystemApp]()
- [ ] Finalize [MandelbrotApp]()
- [ ] Finalize [PDEApp]()
- [ ] Finalize [ConvolutionApp]()
- [ ] Find nice additional visualisations

### Embedding
The next task is embedding the apps, which are currently running with the Bokeh GUI into html pages
- [ ] Minimal embedding example
- [ ] Embed all existing apps in nice html

### Virtual machine
- [x] Get VM running
- [x] Run app locally on VM
- [x] Publish app from VM
- [ ] Publish some html from VM
