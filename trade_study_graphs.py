import numpy as np
import math


# TODO: check units for....basically everything
# TODO: also, check equations and see what the proper equation for supersonic flight is...I just kinda guesseed
def takeoffWeight(SFC_subsonic, SFC_supersonic, L2D_max, R_subsonic, R_supersonic, E):
    # SFC values in 1/hr units
    # L2D is unitless
    # ranges are in mi
    # endurance is in hr
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
    # SUBSONIC:
    # subsonic cruise velocity
    V_c = 600  # mph
    # max lift to drag ratio
    # cruise lift to drag ratio
    L2D_cruise = 0.866 * L2D_max
    L2D_loiter = L2D_max

    # SUPERSONIC:
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
    frac_subsonic = math.exp(-R_subsonic * SFC_subsonic / (V_c * L2D_cruise))
    # supersonic cruise
    frac_supersonic = math.exp(-R_supersonic * SFC_supersonic / (V_super * L2D_super))
    # loiter
    frac_loiter = math.exp(-E * SFC_subsonic / L2D_max)
    # landing
    frac_landing = 0.995
    fuel_fraction = (
        1
        - frac_taxi
        * frac_climb
        * frac_subsonic
        * frac_supersonic
        * frac_loiter
        * frac_landing
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
    # return the final calculated weight
    return weights_calc[-1]


# basic_specs:
parameters_dictionary = {
    "SFC_subsonic": 0.9,
    "SFC_supersonic": 1.5,
    "L2D_max": 16.6,
    "R_subsonic": 1200,
    "R_supersonic": 75,
    "E": 1 / 2,
}
W0_accumiliation = {
    "SFC_subsonic": [],
    "SFC_supersonic": [],
    "L2D_max": [],
    "R_subsonic": [],
    "R_supersonic": [],
    "E": [],
}

# vary all parameter
for parameter in [
    "SFC_subsonic",
    "SFC_supersonic",
    "L2D_max",
    "R_supersonic",
    "R_subsonic",
    "E",
]:
    W0 = []
    if parameter != "L2D_max":
        val_range = np.arange(
            0.75 * parameters_dictionary[parameter],
            1.25 * parameters_dictionary[parameter] + 0.01,
            parameters_dictionary[parameter] / 10,
        )
    else:
        val_range = np.arange(
            0.9 * parameters_dictionary[parameter],
            1.5 * parameters_dictionary[parameter] + 0.01,
            parameters_dictionary[parameter] / 10,
        )

    for val in val_range:
        kwargs = parameters_dictionary
        kwargs.update({parameter: val})
        W0.append(takeoffWeight(**kwargs))
    W0_accumiliation[parameter] = W0

print(W0_accumiliation)
