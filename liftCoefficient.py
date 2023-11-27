import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def lift_coeff_estimate(W0):
    # W0 is input in lbf

    AR_wetted = 1.4  # from text
    K_LD = 14
    L2D_max = K_LD * np.sqrt(AR_wetted)
    # cruise lift to drag ratio
    L2D_cruise = 0.866 * L2D_max
    L2D_super = 0.5 * L2D_max

    SFC = 0.9  # in 1/hr
    Range = 1200  # in mi
    V_c = 600  # in mph

    # find the average weight during cruise
    W_cruise_initial = 0.97 * 0.985 * W0
    W_cruise_final = W_cruise_initial * math.exp(-Range * SFC / (V_c * L2D_cruise))
    W_cruise = (W_cruise_final + W_cruise_initial) / 2

    W_super_initial = W_cruise_final
    R_super = 75  # in mi
    SFC_super = 1.5  # in 1/hr
    Temp_cruise = 390  # degrees R
    M_super = 1.25  # Supersonic Mach No.
    gamma = 1.4
    gas_constant = 1716  # ft-lbf/slug-R
    V_super = M_super * np.sqrt(gamma * gas_constant * Temp_cruise)  # in ft/s
    W_super_final = W_super_initial * math.exp(
        -R_super * SFC_super / (V_super * L2D_super)
    )

    W_super = (W_super_initial + W_super_final) / 2

    # wing sizing
    bw = 28  # wing span in ft
    S_wing = 252  # wing area in ft^2
    AR_wing = bw**2 / S_wing

    # characteristics at flight altitude
    density = 3.64 * 10 ** (-4)  # density at 50,000 ft in slug/ft^3
    dynamicPress = 0.5 * density * V_c**2
    C_L = W_cruise * (1 + 2 / AR_wing) / (dynamicPress * S_wing)

    dynamicPress_super = 0.5 * density * V_super**2
    C_L_super = W_super * (1 + 2 / AR_wing) / (dynamicPress_super * S_wing)
    return [C_L, C_L_super]


# takeoff_weight = np.arange(3000, 10001, 10)
# lift_coeff = []
# for weight in takeoff_weight:
#     lift_coeff.append(lift_coeff_estimate(weight))
#
# plt.plot(takeoff_weight, lift_coeff)
# plt.xlabel("Takeoff Weight [lbf]")
# plt.ylabel("Required Lift Coefficient")
# plt.show()

takeoff_weight = 9839
lift_coeff = lift_coeff_estimate(takeoff_weight)
print("The required lift coefficient is: ", lift_coeff[0])
print("The required supersonic lift coefficient is: ", lift_coeff[1])

# calculate the Reynold's number
V = 600 * 1.467  # cruise velocity in ft/s
c = 9  # chord in feet
# at 50,000 ft: nu = 2.969 * 10 ** (-7) / (3.64 * 10 ** (-4))
nu = 2.969 * 10 ** (-7) / (4.62 * 10 ** (-4))
Re = V * c / nu
print("The Reynold's number is: ", Re)

a = math.sqrt(1.4 * 1717 * 389.97)  # in ft/s
M = V / a
print("The subsonic Mach number is: ", M)

print("The supersonic Mach number is: ", 1.25)


def find_critical_Mach(guess):
    gamma = 1.4
    cp0 = -0.8
    m_crit = guess[0]
    error = (2 / (gamma * m_crit**2)) * (
        ((1 + ((gamma - 1) / 2) * m_crit**2) / (1 + ((gamma - 1) / 2)))
        ** (gamma / (gamma - 1))
        - 1
    ) - cp0 / math.sqrt(1 - m_crit**2)
    return error


critical_mach = fsolve(find_critical_Mach, np.array([0.99999]))

print("The critical Mach number is: ", critical_mach[0])

leading_angle = math.acos(critical_mach[0] / 0.909)
leading_angle_test = math.acos(0.76 / 0.909)
print("The sweep angle is: ", leading_angle_test * 180 / math.pi, "deg")
