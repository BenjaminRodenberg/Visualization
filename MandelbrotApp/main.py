import mandel_config
from mandel_par import mandel
from bokeh.plotting import figure, show, output_file

iterate_max = mandel_config.iterate_max

x_res = mandel_config.x_res
y_res = mandel_config.y_res
x0 = mandel_config.x0
y0 = mandel_config.y0
xw = mandel_config.xw
yw = mandel_config.yw


output_file("mandel.html", title="Mandelbrot Set")

z = mandel(x0, y0, xw, yw, x_res, y_res, iterate_max)

p = figure(x_range=[x0,x0+xw], y_range=[y0,y0+yw], width=x_res, height=y_res)
p.image(image=[z], x=[x0], y=[y0], dw=[xw], dh=[yw], palette="Spectral11")

show(p)  # open a browser

