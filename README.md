# Visualization
Webbased visualization for math content via Bokeh
This Repository contains different prototypes for WebApps for the visualization of math content for lectures at TUM (Technische Universität München).

## Running
### Local
For running the an app, type
```
bokeh serve filename.py
```
and navigate to the respective site.

### Internet
For publishing all apps to the internet run the same command with the option
```
--host <globalip>:5006
```
for accepting connections to the server. All apps can be run using the ```bokeh-runner``` script with the corresponding ```<globalip>```.

## ToDos
### Next Tasks
- [ ] see [LeibnitzApp](https://github.com/BenjaminRueth/Visualization/tree/master/LeibnitzApp)
- [ ] see [FourierApp](https://github.com/BenjaminRueth/Visualization/tree/master/FourierApp)
- [ ] see [ConvolutionApp](https://github.com/BenjaminRueth/Visualization/tree/master/ConvolutionApp)
- [x] see [ODESystemApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODESystemApp)
- [x] see [PDEApp](https://github.com/BenjaminRueth/Visualization/tree/master/PDEApp)
- [ ] do documentation on Bokeh with example App ([MandelbrotApp](https://github.com/BenjaminRueth/Visualization/tree/master/MandelbrotApp)?)

### Generate Running version of particular Apps
- [x] [BoundaryValApp](https://github.com/BenjaminRueth/Visualization/tree/master/BoundaryValApp)
- [x] [ODEApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODEApp)
- [x] [FourierApp](https://github.com/BenjaminRueth/Visualization/tree/master/FourierApp)
- [x] [ODESystemApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODESystemApp)
- [x] [MandelbrotApp](https://github.com/BenjaminRueth/Visualization/tree/master/MandelbrotApp)
- [x] [PDEApp](https://github.com/BenjaminRueth/Visualization/tree/master/PDEApp)
- [x] [ConvolutionApp](https://github.com/BenjaminRueth/Visualization/tree/master/ConvolutionApp)
- [x] [LeibnitzApp](https://github.com/BenjaminRueth/Visualization/tree/master/LeibnitzApp)
- [x] [ArcLengthApp](https://github.com/BenjaminRueth/Visualization/tree/master/ArcLengthApp)
- [ ] [TaylorApp](https://github.com/BenjaminRueth/Visualization/tree/master/TaylorApp)
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
