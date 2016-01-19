from __future__ import division


# all imports have to be done using absolute imports -> that's a bug of bokeh which is know and will be fixed.
def import_bokeh(relative_path):
    import imp
    import os
    app_root_dir = os.path.dirname(os.path.realpath(__file__))
    return imp.load_source('', app_root_dir + '/' + relative_path)


# import local modules
bv_settings = import_bokeh('boundaryVal_settings.py')

def prepareImgBokehRGBA(img):

    import numpy as np

    if img.ndim > 2: # could also be img.dtype == np.uint8
        if img.shape[2] == 3: # alpha channel not included
            img = np.dstack([img, np.ones(img.shape[:2], np.uint8) * 255])
        img = np.squeeze(img.view(np.uint32))
    return img


def drawImage(fig,img,x,y,scale_x,scale_y):
    img = prepareImgBokehRGBA(img)
    fig.image_rgba(image=[img[::-1,:]], x=[x], y=[y],
                   dw=[img.shape[1]/img.shape[1]*scale_x],
                   dh=[img.shape[0]/img.shape[1]*scale_y])
    print img.shape


def drawCannon(fig):
    from scipy import ndimage
    import os

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'Pictures/cannon.png')
    img = ndimage.imread(filename)
    scaling_cannon = 60
    scaling_cannon_x = scaling_cannon*(bv_settings.max_x-bv_settings.min_x)/bv_settings.fig_width
    scaling_cannon_y = scaling_cannon*(bv_settings.max_y-bv_settings.min_y)/bv_settings.fig_height
    x = -0.5*img.shape[1]/img.shape[1]*scaling_cannon_x
    y = -0.5*img.shape[0]/img.shape[1]*scaling_cannon_y
    print "drawing cannon..."
    drawImage(fig,img,x,y,scaling_cannon_x,scaling_cannon_y)
    print "cannon finished."


def drawTargetAt(fig,xTarget):
    from scipy import ndimage
    import os

    scaling_target = 30
    scaling_target_x = scaling_target*(bv_settings.max_x-bv_settings.min_x)/bv_settings.fig_width
    scaling_target_y = scaling_target*(bv_settings.max_y-bv_settings.min_y)/bv_settings.fig_height

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'Pictures/target.png')
    img = ndimage.imread(filename)

    x = xTarget-.5*img.shape[1]/img.shape[1]*scaling_target_x
    y = -.5*img.shape[0]/img.shape[1]*scaling_target_y
    print "drawing target..."
    drawImage(fig,img,x,y,scaling_target_x,scaling_target_y)
    print "target finished."        