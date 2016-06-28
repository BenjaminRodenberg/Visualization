import numpy as np

def shootODE(t,x):
#==============================================================================
#     ODE for shooting an object through the air.
#     saved in x: [rx,ry,vx,vy]
#==============================================================================
    dx=np.empty(4);    
    
    g=-9.81;
    
    #rx=x[0];
    #ry=x[1];
    vx=x[2];
    vy=x[3];
    
    drx=vx;
    dry=vy;
    dvx=0;
    dvy=g;
    
    dx[:] = [drx,dry,dvx,dvy];    
    return dx;
    
def shootAlpha(alpha):
#==============================================================================
#   performs the calculations for shooting an object with a given angle alpha.
#   The arrays with the data of the shoot [rx,ry,vx,vy] and the corresponding
#   time t are returned.
#   The initial velocity, stopping criteria, step width... are hard coded!
#==============================================================================
    h = .001
    v0= 10
    
    #initial conditions 
    rx0=0.0
    ry0=0.0
    vx0=v0*np.cos(alpha*2*np.pi/360.0)
    vy0=v0*np.sin(alpha*2*np.pi/360.0)
    x=np.array([rx0,ry0,vx0,vy0])
    x.shape=(4,1)
    t=np.array([0])
    
    while x[1,-1]>0 or x[3,-1]>0 : #has not hit ground with negative vy
        [t,x]=explEulerStep(shootODE,t,x,h)
        
    return t,x
        
def explEulerStep(f,t,x,h):
#==============================================================================
#     performs one euler step with all the necessary overhead, manipulation of
#     arrays etc...
#==============================================================================
    xnew = x[:,-1]+h*f(t[-1],x[:,-1]);
    xnew = np.reshape(xnew,[4,1]);
    tnew = np.array([t[-1]+h]);
    x = np.concatenate((x,xnew),1);
    t = np.concatenate((t,tnew),0);
    return t,x;   
    
def shootError(xTarget,x):
#==============================================================================
#   calculates the error of a shoot on the target at xTarget. A positive sign
#   of the error indicates that the shoot has been to far, a negative sign that
#   it has been to short.
#==============================================================================    
    xHit = x[0,-1];
    error = xHit - xTarget;    
    return error;  

def plotTrajectory(fig,x):
    fig.line(x[0,:],x[1,:]);
        