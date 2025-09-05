import numpy as np

def gom_nowater():
    thick = [200, 200, 200, 200, 200, 800]
    vp = [1804.65, 1881.82, 1958.98, 2036.14, 2113.31, 4480]
    vs = [1041.92, 1086.47, 1131.02, 1175.57, 1220.12, 2500]
    rho = [2250, 2250, 2250, 2250, 2250, 2100]
    return thick, vp, vs, rho

def gom_nowater_depthadjusted():
    thick = [800,200, 200, 200, 200, 200, 800]
    vp = [1804.65,1804.65, 1881.82, 1958.98, 2036.14, 2113.31, 4480]
    vs = [1041.92,1041.92, 1086.47, 1131.02, 1175.57, 1220.12, 2500]
    rho = [2250,2250, 2250, 2250, 2250, 2250, 2100]
    return thick, vp, vs, rho

def gom_water():
    thick = [800,200, 200, 200, 200, 200, 800]
    vp = [1500,1804.65, 1881.82, 1958.98, 2036.14, 2113.31, 4480]
    vs = [0.001,1041.92, 1086.47, 1131.02, 1175.57, 1220.12, 2500]
    rho = [1000,2250, 2250, 2250, 2250, 2250, 2100]
    return thick, vp, vs, rho

def toy():
    thick = [50, 50, 100, 100]
    vp = [2800, 3000, 3500, 4000]
    vs = [v/2 for v in vp] 
    rho = [1740 * ((v/1000)**0.25) for v in vp]
    return thick, vp, vs, rho

def ice_homo():
    thick = [50, 50, 50, 250]
    vp = [3500, 3500, 3500, 4000]
    vs = [1750, 1750, 1750, 2000]
    rho = [930, 930, 930, 2600]
    return thick, vp, vs, rho

def svalbard():
    thick = [80, 60, 250]
    vp = [3750, 3630, 4850]
    vs = [v/2.12 for v in vp] 
    vs = [1769, 1680, 2425] 
    rho = [930, 930, 2600]
    return thick, vp, vs, rho

def lovenbreen():
    thick = [120, 30, 250]
    vp = [3750, 3630, 4850]
    vs = [v/2.12 for v in vp]
    rho = [930, 930, 2600]
    return thick, vp, vs, rho

def ice_layered():
    thick = [10, 20, 110, 250]
    vp = [3000, 3200, 3500, 4000]
    vs = [1500, 1600, 1750, 2000]
    rho = [930, 930, 930, 2600]
    return thick, vp, vs, rho

def firnbase():
    thick = [20, 10, 120, 250]
    vp = [2900, 2900, 3500, 4000]
    vs = [1300, 1150, 1750, 2000]
    rho = [700, 930, 930, 2600]
    return thick, vp, vs, rho

def firnbasemod():
    thick = [20, 10, 120, 250]
    vs = [1300, 1150, 1750, 2000]
    vp = [v*2 for v in vs]
    rho = [700, 930, 930, 2600]
    return thick, vp, vs, rho

def firndeep():
    thick = [40, 10, 100, 250]
    vp = [2900, 2900, 3500, 4000]
    vs = [1300, 1150, 1750, 2000]
    rho = [700, 930, 930, 2600]
    return thick, vp, vs, rho

def firnthick():
    thick = [20, 20, 110, 250]
    vp = [2900, 2900, 3500, 4000]
    vs = [1300, 1150, 1750, 2000]
    rho = [700, 930, 930, 2600]
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
    

