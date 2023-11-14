import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def lift_coeff_estimate(W0):
    # W0 is input in lbf

    CL_est = 14  # dimensionless
    SFC = 0.9  # in 1/hr
    Range = 1200  # in mi
    V_c = 600  # in mph

    # find the average weight during cruise
    W_cruise_inital = 0.97 * 0.985 * W0
    W_cruise_final = math.exp(-Range * SFC / (V_c * CL_est))
    W_cruise = (W_cruise_final + W_cruise_inital) / 2

    # wing sizing
    bw = 28  # wing span in ft
    S_wing = 252  # wing area in ft^2
    AR_wing = bw**2 / S_wing

    # characteristics at flight altitude
    density = 3.64 * 10 ** (-4)  # density at 50,000 ft in slug/ft^3
    dynamicPress = 0.5 * density * V_c**2
    C_L = W_cruise * (1 + 2 / AR_wing) / (dynamicPress * S_wing)
    return C_L


# takeoff_weight = np.arange(3000, 10001, 10)
# lift_coeff = []
# for weight in takeoff_weight:
#     lift_coeff.append(lift_coeff_estimate(weight))
#
# plt.plot(takeoff_weight, lift_coeff)
# plt.xlabel("Takeoff Weight [lbf]")
# plt.ylabel("Required Lift Coefficient")
# plt.show()

takeoff_weight = 9831
lift_coeff = lift_coeff_estimate(takeoff_weight)
print("The required lift coefficient is: ", lift_coeff)

# calculate the Reynold's number
V = 600 * 1.467  # cruise velocity in ft/s
c = 9  # chord in feet
nu = 2.969 * 10 ** (-7) / (3.64 * 10 ** (-4))
Re = V * c / nu
print("The Reynold's number is: ", Re)

a = math.sqrt(1.4 * 1717 * 389.97)  # in ft/s
M = V / a
print("The Mach number is: ", M)


def find_critical_Mach(guess):
    gamma = 1.4
    cp0 = -1
    guess = guess[0]
    error = (2 / (gamma * guess**2)) * (
        ((1 + ((gamma - 2) / 2) * guess**2) / (1 + ((gamma - 1) / 2)))
        ** (gamma / (gamma - 1))
        - 1
    ) - cp0 / math.sqrt(1 - guess**2)
    return error


critical_mach = fsolve(find_critical_Mach, np.array([0.9]))

print("The critical Mach number is: ", critical_mach[0])
