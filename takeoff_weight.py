import numpy as np
import math
from scipy.optimize import fsolve

# save this reference: https://www.grc.nasa.gov/www/k-12/airplane/sfc.html


def initial_weight_estimate(
    temp_cruise,
    R_sub,
    R_super,
    SFC,
    SFC_super,
    V_c,
    M_super,
    combat_length,
    loiter_length,
    num_crew,
    w_payload,
):
    # ranges in miles, SFC in 1/hr, Mach number is dimensionless, density in slug/ft^3, combat and loiter length in hr,
    # temperatures in deg R, velocity in mph

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # guess W_0
    W_guess = 7000.15  # in lbs from the Talon T-38

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # basic parameters:
    # max lift to drag ratio
    A_wetted = 1.2  # from Raymer figure 3.4
    K_LD = 14
    L2D_max = K_LD * np.sqrt(A_wetted)
    # cruise lift to drag ratio
    L2D_cruise = 0.866 * L2D_max
    L2D_super = 0.25 * L2D_max

    # supersonic cruise velocity
    gamma = 1.4  # dimensionless
    gas_constant = 1716  # ft-lbf/slug-R
    V_super = M_super * np.sqrt(gamma * gas_constant * temp_cruise) * 0.682  # in mph

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # fuel fraction:
    # taxi and take-off
    frac_taxi = 0.97
    # climb
    frac_climb = 0.985
    # subsonic cruise
    frac_subsonic = math.exp(-R_sub * SFC / (V_c * L2D_cruise))
    # supersonic cruise
    frac_supersonic = math.exp(-R_super * SFC_super / (V_super * L2D_super))
    # combat
    frac_combat = math.exp(-combat_length * SFC / L2D_max)
    # loiter
    frac_loiter = math.exp(-loiter_length * SFC / L2D_max)
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
    W_crew = 175 * num_crew
    W_payload = w_payload

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
            self.overleaf_table = " "
            self.counter = 0

        def takeoff_weight(self, W0_guess):
            self.counter = self.counter + 1
            W0_guess = W0_guess[0]
            self.list.append(np.round(W0_guess, decimals=2))
            self.overleaf_table = (
                self.overleaf_table
                + str(np.round(self.counter, decimals=2))
                + " & "
                + str(np.round(W0_guess, decimals=2))
                + " & "
            )
            if W0_guess < 0:
                err = 100
            else:
                empty_weight_frac = weight_ratio(W0_guess)
                W_new = (W_crew + W_payload) / (1 - fuel_fraction - empty_weight_frac)
                self.overleaf_table = (
                    self.overleaf_table
                    + str(np.round(empty_weight_frac, decimals=2))
                    + " & "
                    + str(np.round(W_new, decimals=2))
                    + " \ "
                )
                err = np.abs(W_new - W0_guess)
            return err

    # using fsolve here since the while loop is having a really hard time converging:
    iterations = IterationTable()
    W_calc = fsolve(iterations.takeoff_weight, np.array([W_guess]))
    iteration_table = iterations.list
    empty_weight = weight_ratio(W_calc[0]) * W_calc[0]

    # print(iterations.overleaf_table)

    takeoff_weight = W_calc[0]
    W_climb = takeoff_weight * frac_taxi
    W_cruise = W_climb * frac_climb
    W_supersonic = W_cruise * frac_subsonic
    W_combat = W_supersonic * frac_supersonic
    W_loiter = W_combat * frac_combat
    W_landing = W_loiter * frac_loiter
    W_final = W_landing * frac_landing

    intermediate_weights = np.array(
        [
            takeoff_weight,
            W_climb,
            W_cruise,
            W_supersonic,
            W_combat,
            W_loiter,
            W_landing,
            W_final,
        ]
    )

    # return statement returns the iteration table, the empty weight, and the weights at the *start*
    # of each mission leg
    return (
        np.round(iteration_table, decimals=2),
        np.round(empty_weight, decimals=2),
        np.round(intermediate_weights, decimals=2),
    )
