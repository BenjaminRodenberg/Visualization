import numpy as np
from bokeh.plotting import \
    figure, \
    output_file

thanks = "Thank you for your attention!"
# create data
t = list(thanks)
x = np.linspace(0, 1, t.__len__())
y = 1-x**2

# plot data
p1 = figure()
p1.text(x,y,t, text_font_size="20pt")
# save and open plot
output_file("thanks.html")