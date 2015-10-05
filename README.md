# Visualization
Webbased visualization for math content via Bokeh

This Repository contains different prototypes for WebApps for the visualization of math content for lectures at TUM (Technische Universität München).

Please also read the pdf file in Fourier/fourierSpecification.pdf on how to use the fourier app.

## Running
### Local
For running all the complete apps type
```
bokeh-server --script run_apps.py
```
and navigate to the respective site

### Internet
For publishing all apps to the internet run
```
redis-server --port 7001
```
Then
```
gunicorn -k tornado -w 4 "bokeh.server.start:make_tornado(config_file='config.py')" --log-level=debug --log-file=- -b 0.0.0.0:5006
```
finally
```
python forwarder.py 
```
gunicorn can be shut down with `pkill -9 gunicorn`. Access the apps by navigating to `<globalip>:5006/bokeh/<appurl>`.

## ToDos
### On particular Apps
- [ ] Find out how to bring an app to the internet ( see [Gallery](http://bokeh.pydata.org/en/latest/docs/gallery.html) ). How to get from an app like [Examples/Stocks](https://github.com/BenjaminRueth/Visualization/tree/master/Examples/ExampleStocks) to an app running in the internet?
- [ ] Finalize [BoundaryValApp](https://github.com/BenjaminRueth/Visualization/tree/master/BoundaryValApp)
- [ ] Finalize [ODEApp](https://github.com/BenjaminRueth/Visualization/tree/master/ODEApp)
- [ ] Finalize [FourierApp](https://github.com/BenjaminRueth/Visualization/tree/master/FourierApp)
- [ ] Find nice additional visualisations

### Local machine
- [x] Publish some html from local machine
- [ ] Find out how to bring an app to the internet running on the local machine ( see [Examples/Stocks](https://github.com/BenjaminRueth/Visualization/tree/master/Examples/ExampleStocks) )
- [ ] Find out if information in the bokeh docu on embedding might be helpful (see [here](http://bokeh.pydata.org/en/latest/docs/user_guide/embed.html#server-data))

### Virtual machine
- [x] Get VM running
- [x] Run app locally on VM
- [ ] Publish some html from VM
- [ ] Publish app from VM
