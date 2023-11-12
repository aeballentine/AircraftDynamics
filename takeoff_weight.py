import numpy as np
import math

# TODO: check units for....basically everything
# TODO: also, check equations and see what the proper equation for supersonic flight is...I just kinda guesseed

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# guess W_0
W_guess = 7165  # in lbs from the Talon T-38
W_old = W_guess
# initial error so that the while loop runs (start error greater than 0.01, or 1%)
error = 1
# array to hold all the calculated takeoff weights -> show improvement over iterations
weights_calc = [W_guess]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# basic parameters:
# SUBSONIC range
R = 1200  # in mi
# subsonic specific fuel consumption
SFC = 0.9  # 1/hr
# subsonic cruise velocity
V_c = 600  # mph
# max lift to drag ratio
AR_wetted = 1.4  # from text
K_LD = 14
L2D_max = K_LD * np.sqrt(AR_wetted)
# cruise lift to drag ratio
L2D_cruise = 0.866 * L2D_max
L2D_loiter = L2D_max

# ENDURANCE
E = 1 / 2  # in hr

# SUPERSONIC range
R_super = 75  # in mi
# supersonic specific fuel consumption
SFC_super = 1.5  # (lbm/hr)/lbf - https://www.grc.nasa.gov/www/k-12/airplane/sfc.html
# Need to convert to 1/hr, getting answer in s^2/(hr*ft) - ask Prof
# supersonic cruise velocity
cruise = 50000  # ft
ceiling = 55000  # ft
Temp_cruise = 390  # degrees R
M_super = 1.25  # Supersonic Mach No.
gamma = 1.4
gas_constant = 287  # J/kgK
V_super = (M_super * np.sqrt(gamma * gas_constant * (Temp_cruise * 0.556))) * 3.28
# converted temp to K, calculated m/s, multiplied by 3.28 to get
L2D_super = 0.5 * L2D_max  # double check formula

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# fuel fraction:
# taxi and take-off
frac_taxi = 0.97
# climb
frac_climb = 0.985
# subsonic cruise
frac_subsonic = math.exp(-R * SFC / (V_c * L2D_cruise))
# supersonic cruise
frac_supersonic = math.exp(-R_super * SFC_super / (V_super * L2D_super))
# loiter
frac_loiter = math.exp(-E * SFC / L2D_max)
# landing
frac_landing = 0.995
fuel_fraction = (
    1
    - frac_taxi * frac_climb * frac_subsonic
    # * frac_supersonic
    * frac_loiter * frac_landing
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# crew and payload weight
W_crew = 175 * 2
W_payload = 0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# empty weight ratio
def weight_ratio(takeoff_weight):
    A = 1.59
    C = -0.10
    empty_weight_ratio = A * takeoff_weight**C
    return empty_weight_ratio


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
while error > 0.01:
    W_new = (W_crew + W_payload) / (1 - fuel_fraction - weight_ratio(W_old))
    error = np.abs(W_new - W_old)
    weights_calc.append(W_new)
    W_old = W_new

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# print the determined weight of the aircraft
print("The empty weight is: ", np.round(weights_calc[-1], decimals=0), "lbs")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# step 4b airfoil selection
AOA_cruise = 2 #degrees
#rho_c = 0.0117 #density at 50k ft cruise in lbf/ft^3
rho_c = 3.63*(10**-4) #density at 50kft cruise in slug/ft^3
q_c = 0.5*rho_c*(V_c*5280*(1/3600))**2 #dynamic pressure with speed in ft/s
b = 28 # wing span in ft
c = 9 #chord length in ft
S_wing = b*c
AR_w = (b**2)/S_wing
W_c = 3589
Cl_req_cruise = (W_c/(q_c*S_wing))*(1+(2/AR_w))
print("Cl required for cruise: ", Cl_req_cruise)
