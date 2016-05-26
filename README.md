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
- [ ] Refactor identical code from different apps into one script in Visualization. Possible parts of the code: Sympy parsing, bokeh interaction, quiver function
- [x] add streaming data update for user view. [FourierApp](https://github.com/BenjaminRueth/Visualization/tree/master/FourierApp)
- [ ] do documentation & Refactoring, where possible.
- [ ] do documentation on Bokeh with example App. Slides? Link to Webpage Tutorial and some additional remarks?

### Proper Documentation & Refactoring (state: running version with nice functionality)
- [ ] [BoundaryValApp](https://github.com/BenjaminRueth/Visualization/tree/master/BoundaryValApp)
- [ ] [ODEApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODEApp)
- [x] [FourierApp](https://github.com/BenjaminRueth/Visualization/tree/master/FourierApp)
- [ ] [ODESystemApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODESystemApp)
- [x] [MandelbrotApp](https://github.com/BenjaminRueth/Visualization/tree/master/MandelbrotApp)
- [ ] [PDEApp](https://github.com/BenjaminRueth/Visualization/tree/master/PDEApp)
- [ ] [ConvolutionApp](https://github.com/BenjaminRueth/Visualization/tree/master/ConvolutionApp)
- [ ] [LeibnitzApp](https://github.com/BenjaminRueth/Visualization/tree/master/LeibnitzApp)
- [ ] [ArcLengthApp](https://github.com/BenjaminRueth/Visualization/tree/master/ArcLengthApp)
- [ ] [TaylorApp](https://github.com/BenjaminRueth/Visualization/tree/master/TaylorApp)

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
