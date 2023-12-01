import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# NOTE: multiple values labeled FIX that need to be checked/updated (based
# on airfoil selection, etc.


def wing_loading(W0):
    # WING LOADING - CRUISE

    # dynamic pressure at cruise
    V_cruise = 880  # ft/s
    density_cruise = 3.64 * 10 ** (-4)  # density at 50,000 ft in slug/ft^3
    q_c = 0.5 * density_cruise * V_cruise**2
    e_0 = 0.8  # typically between 0.7 and 0.85
    # wing dimensions
    b_w = 28  # wing span in ft
    S_w = 252  # wing area in ft^2
    AR_w = b_w**2 / S_w
    # lift to drag at cruise
    AR_wetted = 1.4  # from text
    K_LD = 14
    L2D_max = K_LD * np.sqrt(AR_wetted)
    L2D_cruise = 0.866 * L2D_max
    L2D_super = 0.5 * L2D_max
    # wing loading at cruise
    R = 1200  # subsonic range in mi
    SFC = 0.9  # subsonic specific fuel consumption 1/hr
    W_cruise_initial = 0.97 * 0.985 * W0
    W_cruise_final = W_cruise_initial * math.exp(-R * SFC / (V_cruise * L2D_cruise))
    W_cruise = 9400  # in lbs
    C_L = W_cruise * (1 + 2 / AR_w) / (q_c * S_w)
    C_D0 = 0.015
    wing_loading_cruise_uncorr = q_c * math.sqrt((C_D0 * math.pi * AR_w * e_0) / 3)

    # WING LOADING - LOITER

    # dynamic pressure at loiter
    V_loiter = 338  # speed in ft/s, =200 knots
    density_loiter = 5.87*10**(-4) #density at 40kft 
    q_l = 0.5 * density_loiter * V_loiter**2
    wing_loading_loiter_uncorr = q_l * math.sqrt(C_D0 * math.pi * AR_w * e_0)
    W_loiter = 7704  # in lbs

    # WING LOADING - LANDING

    density_SL = 0.00238  # density at SL in slug/ft^3
    C_Lmax = 2.2  # Maximum CL for SC(2)-0714
    W_landing = 7317  # in lbf
    V_stall = math.sqrt(2 * W_landing / (density_SL * S_w * C_Lmax))
    q_landing = 0.5 * density_SL * V_stall**2
    wing_loading_landing_uncorr = C_Lmax * S_w * q_landing
    W_landing = 7497  # in lbs

    # WING LOADING - TAKEOFF

    density_airport = density_SL  # need to change?
    S_g = 2500  # takeoff dist in ft based on baseline aircraft
    TOP = 160  # based on S_g and Fig. 5.4
    sigma = density_airport / density_SL
    C_LTO = C_Lmax
    M_max = 1.25
    thrust_weight_TO = 0.488 * M_max**0.728  # table 5.3
    wing_loading_TO_uncorr = TOP * sigma * C_LTO * thrust_weight_TO
    W_TO = 9543  # new takeoff weight?

    # WING LOADING - COMBAT / SUPERSONIC
    temp_cruise = 390  # degrees R
    M_super = 1.25
    gamma = 1.4
    gas_constant = 1716  # ft-lbf/slug-R
    V_super = M_super * np.sqrt(gamma * gas_constant * temp_cruise)  # in ft/s
    q_super = 0.5*density_cruise*(V_super)**2
    wing_loading_supersonic_uncorr = q_super * math.sqrt((C_D0 * math.pi * AR_w * e_0) / 3)

    # Supersonic details
    R_super = 396000  # ft
    SFC_super = 1.5/3600  # in 1/sec
    W_super_initial = W_cruise_final
    W_super_final = W_super_initial * math.exp(-R_super * SFC_super / (V_super * L2D_super))
    W_super = (W_super_initial + W_super_final) / 2

    # CORRECTED WING LOADINGS
    wing_loading_cruise_corr = wing_loading_cruise_uncorr * (W0/W_cruise)
    wing_loading_loiter_corr = wing_loading_loiter_uncorr * (W0/W_loiter)
    wing_loading_landing_corr = wing_loading_landing_uncorr * (W0/W_landing)
    wing_loading_TO_corr = wing_loading_TO_uncorr
    wing_loading_supersonic_corr = wing_loading_supersonic_uncorr * (W0/W_super)                                                     
                                                    

    # Display uncorrected wing loadings
    print("Uncorrected wing loading at cruise: ", wing_loading_cruise_uncorr, 'lb/ft^2')
    print('Uncorrected wing loading at loiter: ', wing_loading_loiter_uncorr, 'lb/ft^2')
    print('Uncorrected wing loading at landing: ', wing_loading_landing_uncorr, 'lb/ft^2')
    print('Uncorrected wing loading at takeoff: ', wing_loading_TO_uncorr, 'lb/ft^2')
    print('Uncorrected wing loading at combat: ', wing_loading_supersonic_uncorr, 'lb/ft^2')
    
    # Display corrected wing loadings
    print("Corrected wing loading at cruise: ", wing_loading_cruise_corr, "lb/ft^2")
    print("Corrected wing loading at loiter: ", wing_loading_loiter_corr, "lb/ft^2")
    print("Corrected wing loading at landing: ", wing_loading_landing_corr, "lb/ft^2")
    print("Corrected wing loading at takeoff: ", wing_loading_TO_corr, "lb/ft^2")
    print('Corrected wing loading at combat: ', wing_loading_supersonic_corr, 'lb/ft^2')

    # REFINED WING AREA
    Sw_TO = W_TO / wing_loading_TO_corr
    Sw_cruise = W_cruise / wing_loading_cruise_corr
    Sw_landing = W_landing / wing_loading_landing_corr
    Sw_loiter = W_loiter / wing_loading_loiter_corr
    print("List of new wing areas: ", Sw_TO, Sw_cruise, Sw_landing, Sw_loiter)
    Sw_refined = max(Sw_cruise, Sw_loiter, Sw_landing, Sw_TO)
    print("Refined wing area: ", Sw_refined, "ft^2")

    print("~~~~~~~~~~~~~~~~~~~~~~")

    # THRUST-WEIGHT RATIO - CRUISE
    thrust_weight_cruise = ((q_c * C_D0) / wing_loading_cruise_uncorr) + (
        wing_loading_cruise_uncorr / (math.pi * AR_w * e_0 * q_c)
    )
    print("Thrust-to-weight ratio at cruise: ", thrust_weight_cruise)
    thrust_cruise = thrust_weight_cruise * W_cruise
    print("Thrust at cruise: ", thrust_cruise, "lb")

    # THRUST-WEIGHT RATIO - LOITER
    thrust_weight_loiter = ((q_l * C_D0) / wing_loading_loiter_uncorr) + (
        wing_loading_loiter_uncorr / (math.pi * q_l * AR_w * e_0)
    )
    # Note: should this be based on wing loading just calculated?
    print("Thrust-to-weight ratio at loiter: ", thrust_weight_loiter)
    thrust_loiter = thrust_weight_loiter * W_loiter
    print("Thrust at loiter: ", thrust_loiter, "lb")

    # THRUST-WEIGHT RATIO - TAKEOFF
    thrust_TO = thrust_weight_TO * W_TO
    print("Thrust-to-weight ratio at takeoff: ", thrust_weight_TO)
    print("Thrust at takeoff: ", thrust_TO, "lb")

    # THRUST-WEIGHT RATIO - LANDING
    thrust_weight_landing = ((q_landing * C_D0) / wing_loading_landing_uncorr) + (
        wing_loading_landing_uncorr / (math.pi * q_landing * AR_w * e_0))
    thrust_landing = thrust_weight_landing * W_landing
    print("Thrust-to-weight ratio at landing: ", thrust_weight_landing)
    print("Thrust at landing: ", thrust_landing, "lb")

    # THRUST-WEIGHT RATIO - COMBAT/SUPERSONIC
    thrust_weight_supersonic = 0.514*M_max**0.141
    print('Thrust-to-weight ratio at combat: ', thrust_weight_supersonic)
    thrust_supersonic = thrust_weight_supersonic * W_super
    print('Thrust at supersonic: ', thrust_supersonic, 'lb')
    #NOTE: used Table 5.3 for supersonic T/W but it says at cruise - should we change?

wing_loading(9830)
