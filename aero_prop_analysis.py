import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# NOTE - Update C_Lmax for new airfoil, update cruise weight after refined estimate

# def prop_analysis():

# Define stall speed and cruise speed, conditions
C_Lmax = 1.7  # Maximum CL for SC2-0414
W_landing = 8461  # TODO
density_SL = 0.00238  # sea level density in slug/ft^3
Sw_refined = 239.911  # refined wing area in ft^2 from wing loading
V_stall = round(math.sqrt(2 * W_landing / (density_SL * Sw_refined * C_Lmax)))  # ft/s
print(V_stall)
V_c_ft = 880  # ft/s
b_w = 28
AR_w = b_w**2 / Sw_refined
e_0 = 1.78 * (1 - (0.045 * AR_w**0.68)) - 0.64  # Refined e_0
W_cruise = 10000  # cruise weight - UPDATE?
density_cruise = 4.62 * 10 ** (-4)  # density at 45000 ft
gamma = 1.4
gas_constant = 1716  # ft-lbf/slug-R
temp_cruise = 390  # degrees R
mu_cruise = 2.969 * 10 ** (-7) / (4.62 * 10 ** (-4))
xc_max = 0.83  # (x/c) maximum
tc = 0.14  # (t/c) ratio
sweep_angle = 35  # degrees
meanchord_wing = 7.095  # ft
meanchord_HT = 3.444  # ft
meanchord_VT = 4.963  # ft
S_HT = 39.884  # ft^2
S_VT = 126.461  # ft^2
W0 = 9830  # TAKEOFF WEIGHT - UPDATE
FL = 0.79 * W0**0.41  # fuselage length - l_k for fuselage
fineness_ratio = 12  # based on pg 157
Df = FL / fineness_ratio  # fuselage diameter - FIX
h_nose = Df
S_wet_noseandback = 2 * math.pi * (Df / 2) * math.sqrt((Df / 2) ** 2 + h_nose**2)

# Solve for velocity range
velocity = []
D_a = []
thrust_cruise = []
for V in range(V_stall, V_c_ft + 1):
    C_L_aircraft = W_cruise / (0.5 * density_cruise * V**2 * Sw_refined)
    C_D_induced = (C_L_aircraft**2) / (math.pi * AR_w * e_0)

    # Wing (imaginary)
    M_wing = V / math.sqrt(gamma * gas_constant * temp_cruise)
    Re_wing = (density_cruise * V * meanchord_wing) / mu_cruise
    C_f_wing = 0.455 / (
        (math.log10(Re_wing) ** 2.58) * (1 + (0.144 * M_wing**2)) ** 0.65
    )
    Ff_wing = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
        1.39 * (M_wing**0.18) * math.cos(sweep_angle) ** 0.28
    )
    S_wet_wing = 2 * Sw_refined
    C_D0_wing = C_f_wing * Ff_wing * (S_wet_wing / Sw_refined)

    # Horizontal Tail (imaginary)
    M_HT = V / math.sqrt(gamma * gas_constant * temp_cruise)
    Re_HT = (density_cruise * V * meanchord_HT) / mu_cruise
    print(Re_HT)
    C_f_HT = 0.455 / ((math.log10(Re_HT) ** 2.58) * (1 + (0.144 * M_HT**2)) ** 0.65)
    print(C_f_HT)
    Ff_HT = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
        1.39 * (M_wing**0.18) * math.cos(sweep_angle) ** 0.28
    )
    print(Ff_HT)
    S_wet_HT = 2 * S_HT
    C_D0_HT = C_f_HT * Ff_HT * (S_wet_HT / Sw_refined)

    # Vertical Tail (imaginary)
    M_VT = V / math.sqrt(gamma * gas_constant * temp_cruise)
    Re_VT = (density_cruise * V * meanchord_VT) / mu_cruise
    C_f_VT = 0.455 / ((math.log10(Re_VT) ** 2.58) * (1 + (0.144 * M_VT**2)) ** 0.65)
    Ff_VT = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
        1.39 * (M_VT**0.18) * math.cos(sweep_angle) ** 0.28
    )
    S_wet_VT = 2 * S_VT
    C_D0_VT = C_f_VT * Ff_VT * (S_wet_VT / Sw_refined)

    # Fuselage (not imaginary)
    f = FL / Df
    M_fuse = V / math.sqrt(gamma * gas_constant * temp_cruise)
    Re_fuse = (density_cruise * V * FL) / mu_cruise
    C_f_fuse = 0.455 / (
        (math.log10(Re_fuse) ** 2.58) * (1 + (0.144 * M_fuse**2)) ** 0.65
    )
    Ff_fuse = 1 + (60 / (f**3)) + (f / 400)
    S_wet_fuse = (math.pi * FL * Df) + S_wet_noseandback
    C_D0_fuse = C_f_fuse * Ff_fuse * (S_wet_fuse / Sw_refined)

    # AIRCRAFT
    C_D0_aircraft = C_D0_wing + C_D0_HT + C_D0_VT + C_D0_fuse
    print("Drag_0 - ", C_D0_aircraft)
    C_D_aircraft = C_D0_aircraft + C_D_induced
    # print('Aircraft drag coefficient C_D_aircraft: ', C_D_aircraft)
    q_cruise = 0.5 * density_cruise * (V**2)
    D_aircraft = C_D_aircraft * q_cruise * Sw_refined
    # print('Aircraft drag D_a', D_aircraft, 'lb')
    velocity.append(V)
    D_a.append(D_aircraft)
    thrust_cruise.append(897.602)  # cruise thrust from step 5

# Plot drag vs. velocity
plt.plot(velocity, D_a, color="blue", label="Drag [lb]")
plt.plot(velocity, thrust_cruise, color="red", label="Cruise Thrust [lb]")
plt.title("Plot of Aircraft Drag and Thrust vs. Flight Speed")
plt.legend()
plt.show()
