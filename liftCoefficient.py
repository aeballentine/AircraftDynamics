import math
import numpy as np


def lift_coeff_estimate(
    V_c,
    W_cruise,
    W_supersonic,
    bw,
    S_wing,
    cruise_density,
    V_super,
    dynamic_visc,
    temp_cruise,
):
    # W0 is input in lbf, ranges in miles and velocity in mph

    # wing sizing
    AR_wing = bw**2 / S_wing

    # characteristics at flight altitude
    V_c_ft = V_c / 0.682
    dynamicPress = 0.5 * cruise_density * V_c_ft**2
    C_L = W_cruise * (1 + 2 / AR_wing) / (dynamicPress * S_wing)

    V_super_ft = V_super / 0.682  # conversion to ft/s
    dynamicPress_super = 0.5 * cruise_density * V_super_ft**2
    C_L_super = W_supersonic * (1 + 2 / AR_wing) / (dynamicPress_super * S_wing)

    # calculate the Reynold's number
    c = 9  # chord in feet
    nu = dynamic_visc / cruise_density
    Re = V_c_ft * c / nu

    a = math.sqrt(1.4 * 1717 * temp_cruise)  # in ft/s
    M_subsonic = V_c_ft / a

    return (
        np.round(C_L, decimals=2),
        np.round(C_L_super, decimals=2),
        np.round(Re, decimals=2),
        np.round(M_subsonic, decimals=2),
    )


# def find_critical_Mach(guess):
#     gamma = 1.4
#     cp0 = -0.8
#     m_crit = guess[0]
#     error = (2 / (gamma * m_crit**2)) * (
#         ((1 + ((gamma - 1) / 2) * m_crit**2) / (1 + ((gamma - 1) / 2)))
#         ** (gamma / (gamma - 1))
#         - 1
#     ) - cp0 / math.sqrt(1 - m_crit**2)
#     return error
#
# critical_mach = fsolve(find_critical_Mach, np.array([0.99999]))

# print("The critical Mach number is: ", critical_mach[0])

# critical_mach = 0.77
# leading_angle = math.acos(critical_mach / 0.909)
# leading_angle_test = math.acos(0.77 / 0.909)
# print("The sweep angle is: ", leading_angle_test * 180 / math.pi, "deg")
