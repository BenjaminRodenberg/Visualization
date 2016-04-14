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
### On particular Apps
- [x] Finalize [BoundaryValApp](https://github.com/BenjaminRueth/Visualization/tree/master/BoundaryValApp)
- [x] Finalize [ODEApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODEApp)
- [x] Finalize [FourierApp](https://github.com/BenjaminRueth/Visualization/tree/master/FourierApp)
- [x] Finalize [ODESystemApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODESystemApp)
- [x] Finalize [MandelbrotApp](https://github.com/BenjaminRueth/Visualization/tree/master/MandelbrotApp)
- [x] Finalize [PDEApp](https://github.com/BenjaminRueth/Visualization/tree/master/PDEApp)
- [x] Finalize [ConvolutionApp](https://github.com/BenjaminRueth/Visualization/tree/master/ConvolutionApp)
- [ ] Finalize [TaylorApp](https://github.com/BenjaminRueth/Visualization/tree/master/TaylorApp)
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
