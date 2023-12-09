import numpy as np
import math
from scipy.optimize import fsolve


def refined_weight_estimate(
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
    L2D_sub,
    L2D_loiter,
    L2D_super,
    L2D_combat,
    M_subsonic,
    T2W,
    AR,
    W2S,
):
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # guess W_0
    W_guess = 10000.15

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # basic parameters:
    gamma = 1.4
    gas_constant = 1716  # ft-lbf/slug-R
    V_super = M_super * np.sqrt(gamma * gas_constant * temp_cruise) * 0.682  # in mph

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~
    # fuel fraction:
    # taxi and take-off
    frac_taxi = 0.97
    # climb
    frac_climb = 0.985
    # subsonic cruise
    frac_subsonic = math.exp(-R_sub * SFC / (V_c * L2D_sub))
    # supersonic cruise
    frac_supersonic = math.exp(-R_super * SFC_super / (V_super * L2D_super))
    # combat
    frac_combat = math.exp(-combat_length * SFC / L2D_combat)
    # loiter
    frac_loiter = math.exp(-loiter_length * SFC / L2D_loiter)
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
    class IterationTable:
        def __init__(self):
            self.list = []
            self.M_max = None
            self.T2W = None
            self.AR = None
            self.W2S = None

        # def weight_ratio(self, W0):
        #     a = -0.02
        #     b = 2.16
        #     C1 = -0.10
        #     C2 = 0.20
        #     C3 = 0.04
        #     C4 = -0.10
        #     C5 = 0.08
        #     k_vs = 1.00
        #     empty_weight_ratio = (
        #         a
        #         + b
        #         * W0**C1
        #         * self.AR**C2
        #         * self.T2W**C3
        #         * self.W2S**C4
        #         * self.M_max**C5
        #     ) * k_vs
        #     return empty_weight_ratio

        @staticmethod
        def weight_ratio(W0):
            A = 2.34  # jet fighter: 2.34  # jet trainer: 1.59
            C = -0.13  # jet fighter: -0.13  # jet trainer: -0.10
            empty_weight_ratio = A * W0**C
            return empty_weight_ratio

        def takeoff_weight(self, W0_guess):
            W0_guess = W0_guess[0]
            self.list.append(np.round(W0_guess, decimals=2))
            if W0_guess < 0:
                err = 100
            else:
                W_new = (W_crew + W_payload) / (
                    1 - fuel_fraction - self.weight_ratio(W0_guess)
                )
                err = np.abs(W_new - W0_guess)
            return err

    iterations = IterationTable()
    iterations.M_max = M_subsonic
    iterations.T2W = T2W
    iterations.AR = AR
    iterations.W2S = W2S
    W_calc = fsolve(iterations.takeoff_weight, np.array([W_guess]))
    iteration_table = iterations.list
    empty_weight = iterations.weight_ratio(W_calc[0]) * W_calc[0]

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
