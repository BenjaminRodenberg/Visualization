# Fourier
Information provided in the [documentation](https://github.com/BenjaminRueth/Visualization/blob/master/FourierApp/Doc/fourierSpecification.pdf)

One can also enter any function for computing its Fourier series. For the input we use `sympy` syntax.

## Running
This app can be run by typing
```
$ bokeh serve fourier_app.py
```
into bash and then open
```
http://localhost:5006/fourier_app
```
in the browser.

## ToDos
- [x] Change structure of the App in the style of the sliders example
- [x] Update to Bokeh 0.11
- [x] Add controls for setting periodicity and interval (e.g. [-pi,pi] or [0,2pi] or [0,2])
- [x] Improve GUI
- [x] make sympy input faster (see convolution app as an example implementation)
- [ ] make coeff and function value computation faster by using fft and matrix computations (see analytical solution in [PDEApp](https://github.com/BenjaminRueth/Visualization/tree/master/PDEApp)).
- [ ] Add code for embedding, such that the app can be published on the internet.
- [ ] Implement dynamic printing of analytical expression in embedded html
