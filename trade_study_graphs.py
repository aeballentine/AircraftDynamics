import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# TODO: check units for....basically everything
# TODO: also, check equations and see what the proper equation for supersonic flight is...I just kinda guesseed
def takeoffWeight(SFC_subsonic, SFC_supersonic, R_subsonic, R_supersonic, L2D_max, E):
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
    gas_constant = 1716  # lbf/slugR
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
    # empty weight ratio OLD CODE - Liz trying to fix it
    #def weight_ratio(takeoff_weight):
    #    A = 2.34
    #    C = -0.13
    #    empty_weight_ratio = A * takeoff_weight**C
    #    return empty_weight_ratio

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    #while error > 0.01:
    #    W_new = (W_crew + W_payload) / (1 - fuel_fraction - weight_ratio(W_old))
    #    error = np.abs(W_new - W_old)
    #    weights_calc.append(W_new)
    #    W_old = W_new

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # return the final calculated weight
    #return weights_calc[-1]

# new code added by Liz from intial weight code
def weight_ratio(takeoff_weight):
    A = 2.34  # jet fighter: 2.34  # jet trainer: 1.59
    C = -0.13  # jet fighter: -0.13  # jet trainer: -0.10
    empty_weight_ratio = A * takeoff_weight**C
    return empty_weight_ratio


def takeoff_weight(W_guess):
    W_guess = W_guess[0]
    if W_guess < 0:
        err = 100
    else:
        W_new = (W_crew + W_payload) / (1 - fuel_fraction - weight_ratio(W_guess))
        err = np.abs(W_new - W_guess)
    return err
W_calc = fsolve(takeoff_weight, np.array([W_guess]))
print("The empty weight is: ", np.round(W_calc[0], decimals=2), "lbs")

# basic_specs:
parameters_dictionary = {
    "SFC_subsonic": 0.9,
    "SFC_supersonic": 1.5,
    "R_subsonic": 1200,
    "R_supersonic": 75,
    "L2D_max": 16.6,
    "E": 1 / 2,
}
W0_accumiliation = {
    "SFC_subsonic": [],
    "SFC_supersonic": [],
    "R_subsonic": [],
    "R_supersonic": [],
    "L2D_max": [],
    "E": [],
}
study_vals = {
    "SFC_subsonic": [],
    "SFC_supersonic": [],
    "R_subsonic": [],
    "R_supersonic": [],
    "L2D_max": [],
    "E": [],
}

# vary all parameters
parameters = [
    "SFC_subsonic",
    "SFC_supersonic",
    "R_subsonic",
    "R_supersonic",
    "L2D_max",
    "E",
]
for param in parameters:
    W0 = []
    if param != "L2D_max":
        val_range = np.arange(
            0.8 * parameters_dictionary[param],
            1.2 * parameters_dictionary[param] + 0.01,
            parameters_dictionary[param] / 10,
        )
    else:
        val_range = np.arange(
            0.9 * parameters_dictionary[param],
            1.1 * parameters_dictionary[param] + 0.01,
            parameters_dictionary[param] / 10,
        )
    study_vals[param] = val_range

    for val in val_range:
        kwargs = parameters_dictionary.copy()
        kwargs[param] = val
        W0.append(takeoffWeight(**kwargs))
    W0_accumiliation[param] = W0


fig, axs = plt.subplots(3, 2)
counter = 0
labels = [
    "Subsonic SFC [1/hr]",
    "Supersonic SFC [1/hr]",
    "Subsonic Range [mi]",
    "Supersonic Range [mi]",
    "Maximum Lift-to-Drag Ratio",
    "Endurance [hr]",
]
for row in [0, 1, 2]:
    for col in [0, 1]:
        param = parameters[counter]
        x_vals = study_vals[param]
        y_vals = W0_accumiliation[param]
        axs[row, col].plot(x_vals, y_vals)
        axs[row, col].set_xlabel(labels[counter])
        axs[row, col].set_ylim([3000, 4000])
        if col == 0:
            axs[row, col].set_ylabel("Takeoff Weight [lbs]")
        counter = counter + 1
plt.show()
