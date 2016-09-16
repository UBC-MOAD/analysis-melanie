import numpy as np
from salishsea_tools import  psu_tools

def isopycnal_forTSplot(s,t):

    # Figure out boudaries (mins and maxs)
    smin = s.min() - (0.01 * s.min())
    smax = s.max() + (0.01 * s.max())
    tmin = t.min() - (0.1 * t.max())
    tmax = t.max() + (0.1 * t.max())
 
    # Calculate how many gridcells we need in the x and y dimensions
    xdim = round((smax-smin)/0.1+1,0)
    ydim = round((tmax-tmin)+1,0)
    print(xdim,ydim) 
    # Create empty grid of zeros
    isop = np.zeros((ydim,xdim))
 
    # Create temp and salt vectors of appropiate dimensions
    ti = np.linspace(1,ydim-1,ydim)+tmin
    si = np.linspace(1,xdim-1,xdim)*0.1+smin
 
    # Loop to fill in grid with densities
    for j in range(0,int(ydim)):
        for i in range(0, int(xdim)):
            isop[j,i]=psu_tools.calculate_density(ti[j],si[i])
 
    isop = isop - 1000 # Substract 1000 to convert to sigma-t

    return isop,si,ti
