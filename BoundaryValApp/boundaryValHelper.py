# -*- coding: utf-8 -*-
from __future__ import division

def prepareImgBokehRGBA(img):
    import numpy as np        
    if img.ndim > 2: # could also be img.dtype == np.uint8
        if img.shape[2] == 3: # alpha channel not included
            img = np.dstack([img, np.ones(img.shape[:2], np.uint8) * 255])
        img = np.squeeze(img.view(np.uint32))
    return img;
    
def drawImage(fig,name,x,y,width):
    from scipy import ndimage
    img = ndimage.imread(name);
    img = prepareImgBokehRGBA(img);    
    fig.image_rgba(image=[img[::-1,:]], x=[x], y=[y], 
              dw=[img.shape[1]/img.shape[1]*width],
              dh=[img.shape[0]/img.shape[1]*width]);
    print img.shape;          
              
def drawCannon(fig):
    scaling_cannon = 1;
    x = -0.5;
    y = -0.5;
    print "drawing cannon..."
    drawImage(fig,'cannon.png',x,y,scaling_cannon);    
    print "cannon finished."
    
def drawTargetAt(fig,xTarget):
    scaling_target = 0.5;
    x = xTarget-.25;
    y = -0.25;
    print "drawing target..."
    drawImage(fig,'target.png',x,y,scaling_target);     
    print "target finished."