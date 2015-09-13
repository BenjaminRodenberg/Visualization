# -*- coding: utf-8 -*-

from __future__ import division

import bokeh.plotting as bp
from boundaryValMath import *
from boundaryValHelper import *      
    
bp.output_file("out.html");

xTarget = 1+np.random.rand()*8;

f1 = bp.figure(plot_width=500, plot_height=500, 
               x_range=[-.5, 10], y_range=[-.5, 10]);

drawCannon(f1);
drawTargetAt(f1,xTarget);

#interval
alpha_left = 0.0;
alpha_right = 45.0;
alpha = alpha_right;

#shoot at lower bound
[t,x]=shootAlpha(alpha_left)
error_left = shootError(xTarget,x);

#shoot at upper bound
[t,x]=shootAlpha(alpha_right)
error_right = shootError(xTarget,x);

#calculate minimum error
current_error = min([abs(error_left),abs(error_right)]);

tol = .01;

while current_error > tol: 
    print "iteration with alpha = "+str(alpha)+" not successful.";    
    
    alpha = (alpha_left + alpha_right)/2;

    print "starting iteration with alpha = "+str(alpha)+".";
       
    t,x = shootAlpha(alpha);        
    error = shootError(xTarget,x);
    
    if error * error_left < 0:
        error_right = error;
        alpha_right = alpha;
    else:
        error_left = error;
        alpha_left = alpha;
    
    plotTrajectory(f1,x)        
    
    print "hit ground at x = "+str(x[0,-1])+".";
    current_error = min([abs(error_left),abs(error_right)]);
    
print "iteration with alpha = "+str(alpha)+" successful."; 

f1.title = 'Schießverfahren';

bp.show(f1)