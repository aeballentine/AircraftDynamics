import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# NOTE: multiple values labeled FIX that need to be checked/updated (based
# on airfoil selection, etc. 

def wing_loading(W0):
    #CRUISE
    #dynamic pressure at cruise
    V_cruise = 600 #mph
    density_cruise = 3.64 * 10 ** (-4)  # density at 50,000 ft in slug/ft^3
    q_c = 0.5*density_cruise*V_cruise**2
    e_0 = 0.8 #typically between 0.7 and 0.85
    #wing dimensions
    b_w = 28  # wing span in ft
    S_w = 252  # wing area in ft^2
    AR_w = b_w**2 / S_w
    #lift to drag at cruise
    AR_wetted = 1.4  # from text
    K_LD = 14
    L2D_max = K_LD * np.sqrt(AR_wetted)
    L2D_cruise = 0.866 * L2D_max
    #weight at cruise
    R = 1200 #subsonic range in mi
    SFC = 0.9 #subsonic specific fuel consumption 1/hr
    W_cruise_initial = 0.97*0.985*W0
    W_cruise_final = W_cruise_initial*math.exp(-R*SFC/(V_cruise*L2D_cruise))
    W_cruise = (W_cruise_final+W_cruise_initial)/2
    C_L = W_cruise * (1 + 2 / AR_w) / (q_c * S_w)
    C_D0 = 0.015
    wing_loading_cruise = q_c*math.sqrt((C_D0*math.pi*AR_w*e_0)/3)

    #LOITER
    #dynamic pressure at loiter
    V_loiter = 287 #speed in ft/s, =170 knots since
                    #should be 150-200 knots - FIX? 
    density_loiter = 5.87*10**(-4) #density at 40kft FIX - FIND LOITER ALT
    q_l = 0.5*density_loiter*V_loiter**2
    wing_loading_loiter = q_l*math.sqrt(C_D0*math.pi*AR_w*e_0)

    #LANDING
    #dynamic pressure at landing
    density_SL = 0.00238 #density at SL in slug/ft^3
    V_stall = 214.133 #check - given as stall speed in specs
    q_landing = 0.5*density_SL*V_stall**2
    #calculate wing loading at landing with C_Lmax
    C_Lmax = 2 #FIX for airfoil selection
    wing_loading_landing = C_Lmax*S_w*q_landing
    
    #TAKEOFF
    density_airport = density_SL #need to change?
    S_g = 2500 #takeoff dist in ft based on baseline aircraft
    TOP = 160 #based on S_g and Fig. 5.4
    sigma = density_airport / density_SL
    C_LTO = C_Lmax
    M_max = 1.25
    t_to_w_to = 0.488*M_max**0.728 #table 5.3
    wing_loading_TO = TOP*sigma*C_LTO*t_to_w_to
    print('Wing loading at cruise: ' wing_loading_cruise)
    print('Wing loading at loiter: ' wing_loading_loiter)
    print('Wing loading at landing: ' wing_loading_landing)
    print('Wing loading at takeoff: ' wing_loading_TO) 
