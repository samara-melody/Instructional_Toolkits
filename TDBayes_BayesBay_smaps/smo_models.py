import numpy as np


def toy_gradient():
    thick = [50, 50, 100, 100]
    vp = [2800, 3000, 3500, 4000]
    vs = [v/2 for v in vp] 
    rho = [1740 * ((v/1000)**0.25) for v in vp]
    return thick, vp, vs, rho

def toy_2layer():
    thick = [150, 250]
    vp = [3500, 4000]
    vs = [v/2 for v in vp] 
    rho = [1740 * ((v/1000)**0.25) for v in vp]
    return thick, vp, vs, rho

def bayesbay_ex():
    thick = [10000, 10000, 15000, 20000, 20000, 20000, 20000, 20000, 0]
    vs = [3380, 3440, 3660, 4250, 4350, 4320, 4315, 4380, 4500]
    vp = [x * 1.77 for x in vs]
    rho = [0.32 * (y) + 0.77 for y in vp]
    return thick, vp, vs, rho    

def bayesbay_ex_meterscale():
    thick = [10, 10, 15, 20, 20, 20, 20, 20, 0]
    vs = [3380, 3440, 3660, 4250, 4350, 4320, 4315, 4380, 4500]
    vp = [x * 1.77 for x in vs]
    rho = [0.32 * y + 770 for y in vp]
    return thick, vp, vs, rho    


def add_layer(rows,start_value,end_value,cols=1):
    # rows = thickness of layer (number of cells per layer)
    # start_value = starting value
    # end_value = endingvalue
    linear_values = np.linspace(start_value, end_value, rows)
    layer = np.tile(linear_values.reshape(-1, 1), (1, cols))
    return layer[::-1]

def generate(thick,vp,vs,rho):
    layers = [add_layer(thick[e], p, p) for e, p in enumerate(vp)]
    vp_out = np.vstack(layers)   
    
    layers = [add_layer(thick[e], s, s) for e, s in enumerate(vs)]
    vs_out = np.vstack(layers)   
    
    layers = [add_layer(thick[e], r, r) for e, r in enumerate(rho)]
    rho_out = np.vstack(layers)  
    
    thick_out = np.ones_like(vp_out[::-1]) # each cell is 1 m thick
    
    return thick_out[::-1], vp_out[::-1], vs_out[::-1], rho_out[::-1]
    

