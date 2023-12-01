import numpy as np
import math
from scipy.optimize import fsolve

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# guess W_0
W_guess = 7000.15  # in lbs from the Talon T-38
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

# COMBAT
Com = 1.25  # in hr

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
gas_constant = 1716  # ft-lbf/slug-R
V_super = M_super * np.sqrt(gamma * gas_constant * Temp_cruise)  # in ft/s
L2D_super = L2D_max  # double check formula

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
# combat
frac_combat = math.exp(-Com * SFC / L2D_max)
# loiter
frac_loiter = math.exp(-E * SFC / L2D_max)
# landing
frac_landing = 0.995

fuel_fraction = 1.06 * (
    1
    - frac_taxi
    * frac_climb
    * frac_subsonic
    * frac_supersonic
    * frac_combat
    * frac_loiter
    * frac_landing
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# crew and payload weight
W_crew = 175 * 2
W_payload = 0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# empty weight ratio
def weight_ratio(W0):
    A = 2.34  # jet fighter: 2.34  # jet trainer: 1.59
    C = -0.13  # jet fighter: -0.13  # jet trainer: -0.10
    empty_weight_ratio = A * W0**C
    return empty_weight_ratio


class IterationTable:
    def __init__(self):
        self.list = []

    def takeoff_weight(self, W0_guess):
        W0_guess = W0_guess[0]
        self.list.append(np.round(W0_guess, decimals=2))
        if W0_guess < 0:
            err = 100
        else:
            W_new = (W_crew + W_payload) / (1 - fuel_fraction - weight_ratio(W0_guess))
            err = np.abs(W_new - W0_guess)
        return err


# using fsolve here since the while loop is having a really hard time converging:
# I tried to run it with everything added in to the code. Basically, it keeps getting negative numbers
# this isn't TOO big of a problem, but it proceeds to make EVERYTHING else imaginary
# ...there is a solution, but it basically entails a REALLY good initial guess, which is way too much effort
iterations = IterationTable()
W_calc = fsolve(iterations.takeoff_weight, np.array([W_guess]))
print("The empty weight is: ", np.round(W_calc[0], decimals=2), "lbs")
print(iterations.list)
empty_weight = weight_ratio(W_calc[0]) * W_calc[0]
print("The empty weight is: ", np.round(empty_weight, decimals=2), "lbs")

initial_weight = W_calc[0]
W_climb = W_calc[0] * frac_taxi
W_cruise = W_climb * frac_climb
W_supersonic = W_cruise * frac_subsonic
W_combat = W_supersonic * frac_supersonic
W_loiter = W_combat * frac_combat
W_landing = W_loiter * frac_loiter
W_final = W_landing * frac_landing

print("The heaviest weight during climb is: ", np.round(W_climb, decimals=2), " lbs")
print("The heaviest weight during cruise is: ", np.round(W_cruise, decimals=2), " lbs")
print(
    "The heaviest weight during supersonic cruise is: ",
    np.round(W_supersonic, decimals=2),
    " lbs",
)
print("The heaviest weight during combat is: ", np.round(W_combat, decimals=2), " lbs")
print("The heaviest weight during loiter is: ", np.round(W_loiter, decimals=2), " lbs")
print(
    "The heaviest weight during landing is: ", np.round(W_landing, decimals=2), " lbs"
)


print(W_calc[0] * (1 - fuel_fraction))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# OLD CODE (***THIS DOES NOT CONVERGE***)
# while error > 0.01:
#     W_new = (W_crew + W_payload) / (1 - fuel_fraction - weight_ratio(W_old))
#     error = np.abs(W_new - W_old)
#     weights_calc.append(W_new)
#     W_old = W_new
#     print(W_old)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# print the determined weight of the aircraft
# print("The empty weight is: ", np.round(weights_calc[-1], decimals=0), "lbs")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# # step 4b airfoil selection
# AOA_cruise = 2  # degrees
# # rho_c = 0.0117-0 #density at 50k ft cruise in lbf/ft^3
# rho_c = 3.63 * (10**-4)  # density at 50kft cruise in slug/ft^3
# q_c = (
#     0.5 * rho_c * (V_c * 5280 * (1 / 3600)) ** 2
# )  # dynamic pressure with speed in ft/s
# b = 28  # wing span in ft
# c = 9  # chord length in ft
# S_wing = b * c
# AR_w = (b**2) / S_wing
# W_c = 3589
# Cl_req_cruise = (W_c / (q_c * S_wing)) * (1 + (2 / AR_w))
# print("Cl required for cruise: ", Cl_req_cruise)
