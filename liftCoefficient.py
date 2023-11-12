import math
import numpy as np
import matplotlib.pyplot as plt


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


takeoff_weight = np.arange(3000, 7001, 10)
lift_coeff = []
for weight in takeoff_weight:
    lift_coeff.append(lift_coeff_estimate(weight))

plt.plot(takeoff_weight, lift_coeff)
plt.xlabel("Takeoff Weight [lbf]")
plt.ylabel("Required Lift Coefficient")
plt.show()
