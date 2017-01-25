from __future__ import division
import numpy as np
from bokeh.properties import Color, Seq, Enum

red = (255,0,0,0)
green = (0,255,0,0)
blue = (0,0,255,0)
alpha = (0,0,0,1)

svg_palette_jet = ['#00008f', '#00009f', '#0000af', '#0000bf', '#0000cf', '#0000df', '#0000ef', '#0000ff', '#000fff',
                   '#001fff', '#002fff', '#003fff', '#004fff', '#005fff', '#006fff', '#007fff', '#008fff', '#009fff',
                   '#00afff', '#00bfff', '#00cfff', '#00dfff', '#00efff', '#00ffff', '#0fffef', '#1fffdf', '#2fffcf',
                   '#3fffbf', '#4fffaf', '#5fff9f', '#6fff8f', '#7fff7f', '#8fff6f', '#9fff5f', '#afff4f', '#bfff3f',
                   '#cfff2f', '#dfff1f', '#efff0f', '#ffff00', '#ffef00', '#ffdf00', '#ffcf00', '#ffbf00', '#ffaf00',
                   '#ff9f00', '#ff8f00', '#ff7f00', '#ff6f00', '#ff5f00', '#ff4f00', '#ff3f00', '#ff2f00', '#ff1f00',
                   '#ff0f00', '#ff0000', '#ef0000', '#df0000', '#cf0000', '#bf0000', '#af0000', '#9f0000', '#8f0000',
                   '#7f0000']
