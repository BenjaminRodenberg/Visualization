import numpy as np

from bokeh.plotting import output_file, figure, show, hplot
from bokeh.models import ColumnDataSource, CustomJS, Rect
from bokeh.models.widgets import Slider

output_file('range_update_callback.html')

N = 4000

x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = [
    "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)
]

source = ColumnDataSource({'x': [], 'y': [], 'width': [], 'height': []})

dummy = Slider(title="dummy", start=-2, end=2)

def whine(attrname, old, new):
    print source.data
    print "oh noooo i have to work :("

for w in [dummy]:
    w.on_change('value', whine)

jscode="""
        var data = source.get('data');
        var start = range.get('start');
        var end = range.get('end');
        data['%s'] = [start + (end - start) / 2];
        data['%s'] = [end - start];
        source.trigger('change');
    """

p1 = figure(title='Pan and Zoom Here', x_range=(0, 100), y_range=(0, 100),
            tools='box_zoom,wheel_zoom,pan,reset', plot_width=400, plot_height=400)
p1.scatter(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)

p1.x_range.callback = CustomJS(
        args=dict(source=source, range=p1.x_range), code=jscode % ('x', 'width'))
p1.y_range.callback = CustomJS(
        args=dict(source=source, range=p1.y_range), code=jscode % ('y', 'height'))

p2 = figure(title='See Zoom Window Here', x_range=(0, 100), y_range=(0, 100),
            tools='', plot_width=400, plot_height=400)
p2.scatter(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)
rect = Rect(x='x', y='y', width='width', height='height', fill_alpha=0.1,
            line_color='black', fill_color='black')
p2.add_glyph(source, rect)

layout = hplot(p1, p2, dummy)
show(layout)