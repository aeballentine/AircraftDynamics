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
wetted_area = 1.2
K_LD = 14
L2D_max = K_LD * np.sqrt(wetted_area)
# cruise lift to drag ratio
L2D_cruise = 0.866 * L2D_max

# ENDURANCE
E = 1 / 2  # in hr

# SUPERSONIC range
R_super = 75  # in mi
# supersonic specific fuel consumption
SFC_super = 0.9  # 1/hr
# supersonic cruise velocity
V_super = 960  # mph
# supersonic lift to drag ratio
L2D_super = 0.5 * L2D_max

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
