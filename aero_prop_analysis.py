import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# NOTE - Update C_Lmax for new airfoil, update cruise weight after refined estimate

def prop_analysis():

    # Define stall speed and cruise speed, conditions
    C_Lmax = 2.2 # Maximum CL for SC(2)-0714 - UPDATE AFTER CHOOSING NEW AIRFOIL
    W_landing = 7317 # lbf
    density_SL = 0.00238 # sea level density in slug/ft^3
    V_stall = math.sqrt(2 * W_landing / (density_SL * S_w * C_Lmax)) # ft/s
    V_cruise = 880 #ft/s
    S_w = 254 # refined wing area in ft^2
    b_w = 28
    AR_w = b_w**2 / S_w
    e_0 = 0.8
    W_cruise = 9400 # cruise weight - UPDATE?
    density_cruise = 4.62*10**(-4) #density at 45000 ft
    
    # Solve for velocity range
    for V in range(V_stall, V_cruise+1): 
        C_L_aircraft = W_cruise / (0.5*density_cruise*V**2*S_w)
        C_D_induced = (C_L_aircraft**2)/(math.pi*AR_w*e_0)
        C_D0_aircraft = 
        print
        
