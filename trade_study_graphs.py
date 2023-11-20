import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import plotly.express as px
import pandas as pd


def takeoffWeight(SFC_subsonic, SFC_supersonic, R_subsonic, R_supersonic, L2D_max, E):
    # SFC values in 1/hr units
    # L2D is unitless
    # ranges are in mi
    # endurance is in hr
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # guess W_0
    W_guess = 7000  # in lbs from the Talon T-38

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
    L2D_super = L2D_max  # double check formula

    # COMBAT
    Com = 1.25  # in hr

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
    # combat
    frac_combat = math.exp(-Com * SFC_subsonic / L2D_max)
    # loiter
    frac_loiter = math.exp(-E * SFC_subsonic / L2D_loiter)
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
    # empty weight ratio OLD CODE - Liz trying to fix it
    def weight_ratio(takeoff_weight):
        A = 2.34
        C = -0.13
        empty_weight_ratio = A * takeoff_weight**C
        return empty_weight_ratio

    def takeoff_weight(W0_guess):
        W0_guess = W0_guess[0]
        if W0_guess < 0:
            err = 100
        else:
            W_new = (W_crew + W_payload) / (1 - fuel_fraction - weight_ratio(W0_guess))
            err = np.abs(W_new - W0_guess)
        return err

    W_calc = fsolve(takeoff_weight, np.array([W_guess]))

    # return the final calculated weight
    return W_calc


# basic_specs:
parameters_dictionary = {
    "SFC_subsonic": 0.9,
    "R_subsonic": 1200,
    "SFC_supersonic": 1.5,
    "R_supersonic": 75,
    "L2D_max": 16.6,
    "E": 1 / 2,
}
W0_accumiliation = {
    "SFC_subsonic": [],
    "R_subsonic": [],
    "SFC_supersonic": [],
    "R_supersonic": [],
    "L2D_max": [],
    "E": [],
}
study_vals = {
    "SFC_subsonic": [],
    "R_subsonic": [],
    "SFC_supersonic": [],
    "R_supersonic": [],
    "L2D_max": [],
    "E": [],
}

# vary all parameters
parameters = [
    "SFC_subsonic",
    "R_subsonic",
    "SFC_supersonic",
    "R_supersonic",
    "L2D_max",
    "E",
]
for param in parameters:
    W0 = []
    # if param != "L2D_max":
    val_range = np.arange(
        0.75 * parameters_dictionary[param],
        1.25 * parameters_dictionary[param] + 0.01,
        parameters_dictionary[param] / 1000,
    )
    # else:
    #     val_range = np.arange(
    #         0.95 * parameters_dictionary[param],
    #         1.05 * parameters_dictionary[param] + 0.01,
    #         parameters_dictionary[param] / 10-,
    #     )
    study_vals[param] = val_range

    for val in val_range:
        kwargs = parameters_dictionary.copy()
        kwargs[param] = val
        W0.append(takeoffWeight(**kwargs)[0])
    W0_accumiliation[param] = W0

fig, axs = plt.subplots(3, 2)
counter = 0
labels = [
    "Subsonic SFC [1/hr]",
    "Subsonic Range [mi]",
    "Supersonic SFC [1/hr]",
    "Supersonic Range [mi]",
    "Maximum Lift-to-Drag Ratio",
    "Endurance [hr]",
]
colors = ["tab:blue", "tab:blue", "tab:red", "tab:red", "tab:purple", "tab:purple"]
ylims = [
    [6500, 10200],
    [6500, 10200],
    [9550, 9650],
    [9550, 9650],
    [7000, 10200],
    [9200, 10100],
]
for row in [0, 1, 2]:
    for col in [0, 1]:
        param = parameters[counter]
        x_vals = study_vals[param]
        y_vals = W0_accumiliation[param]
        axs[row, col].plot(x_vals, y_vals, color=colors[counter])
        axs[row, col].set_xlabel(labels[counter])
        axs[row, col].vlines(
            parameters_dictionary[param], 0, 20000, color="black", linestyle="--"
        )
        axs[row, col].set_ylabel("Takeoff Weight [lbs]")
        axs[row, col].set_ylim(ylims[counter])
        counter = counter + 1
plt.show()
