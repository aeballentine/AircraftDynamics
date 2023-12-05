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
# lift to drag ratios:
L2D_sub = 0.101 ** (-1)
L2D_super = 0.53 ** (-1)
L2D_loiter = 0.088 ** (-1)
L2D_combat = 0.53 ** (-1)

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
M_super = 1.25  # supersonic Mach No.
gamma = 1.4
gas_constant = 1716  # ft-lbf/slug-R
V_super = M_super * np.sqrt(gamma * gas_constant * Temp_cruise) * 0.682  # in mph

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# fuel fraction:
# taxi and take-off
frac_taxi = 0.97
# climb
frac_climb = 0.985
# subsonic cruise
frac_subsonic = math.exp(-R * SFC / (V_c * L2D_sub))
# supersonic cruise
frac_supersonic = math.exp(-R_super * SFC_super / (V_super * L2D_super))
# combat
frac_combat = math.exp(-Com * SFC / L2D_combat)
# loiter
frac_loiter = math.exp(-E * SFC / L2D_loiter)
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
print(fuel_fraction)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# crew and payload weight
W_crew = 175 * 2
W_payload = 0


# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# empty weight ratio
def weight_ratio(W0, AR, T2W0, W02S, M_max):
    a = -0.02
    b = 2.16
    C1 = -0.10
    C2 = 0.20
    C3 = 0.04
    C4 = -0.10
    C5 = 0.08
    k_vs = 1.00
    empty_weight_ratio = (
        a + b * W0**C1 * AR**C2 * T2W0**C3 * W02S**C4 * M_max**C5
    ) * k_vs
    print(empty_weight_ratio)
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
            M_max = 0.909
            T2W = 0.574  # max thrust to weight
            AR = 6.5
            W2S = 29
            W_new = (W_crew + W_payload) / (
                1 - fuel_fraction - weight_ratio(W0_guess, AR, T2W, W2S, M_max)
            )
            err = np.abs(W_new - W0_guess)
        return err


iterations = IterationTable()
W_calc = fsolve(iterations.takeoff_weight, np.array([W_guess]))
print("The empty weight is: ", np.round(W_calc[0], decimals=2), "lbs")
print(iterations.list)
# empty_weight = weight_ratio(W_calc[0]) * W_calc[0]
# print("The empty weight is: ", np.round(empty_weight, decimals=2), "lbs")
