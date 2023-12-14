import math
import numpy as np
import matplotlib.pyplot as plt

# NOTE - update cruise weight after refined estimate
# todo: supersonic wave drag


def propulsion_analysis(
    c_l_max,
    w_landing,
    cruise_density,
    S_wing,
    V_c,
    AR_wing,
    M_super,
    w_cruise,
    takeoff_weight,
    cruise_temp,
    Re_wing,
    xc_max,
    tc,
    sweep_angle,
    c_h_tail,
    c_v_tail,
    S_h_tail,
    S_v_tail,
    fuselage_length,
    M_subsonic,
    dynamic_visc,
    cruise_thrust,
):
    # Define stall speed and cruise speed, conditions
    # density_SL = 0.00238  # sea level density in slug/ft^3
    V_stall = round(
        math.sqrt(2 * w_landing / (cruise_density * S_wing * c_l_max))
    )  # ft/s
    V_c_ft = round(V_c / 0.682)  # ft/s
    # b_w = 29.5
    e_0 = 1.78 * (1 - (0.045 * AR_wing**0.68)) - 0.64  # Refined e_0
    gamma = 1.4
    gas_constant = 1716  # ft-lbf/slug-R
    # mu_cruise = 2.969 * 10 ** (-7)  # / (4.62 * 10 ** (-4))
    V_super = M_super * math.sqrt(gamma * gas_constant * cruise_temp)
    sweep_angle = sweep_angle * np.pi / 180  # conversion to radians
    fineness_ratio = 12  # based on pg 157
    Df = fuselage_length / fineness_ratio  # fuselage diameter - FIX
    h_nose = Df
    S_wet_noseandback = 2 * math.pi * (Df / 2) * math.sqrt((Df / 2) ** 2 + h_nose**2)

    # Solve for velocity range
    velocity = []
    D_a = []
    thrust_cruise = []
    for V in range(V_stall, round(1.2 * V_super) + 1):
        q_cruise = 0.5 * cruise_density * (V**2)
        C_L_aircraft = w_cruise / (q_cruise * S_wing)
        C_D_induced = (C_L_aircraft**2) / (math.pi * AR_wing * e_0)
        # print('CD induced: ', C_D_induced)

        # Wing
        M_wing = M_subsonic  # todo: do we need to multiply this by the sweep angle?
        # Re_wing = (density_cruise * V * meanchord_wing) / mu_cruise
        C_f_wing = 0.455 / (
            (math.log10(Re_wing) ** 2.58) * (1 + (0.144 * M_wing**2)) ** 0.65
        )
        Ff_wing = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
            1.39 * (M_wing**0.18) * math.cos(sweep_angle) ** 0.28
        )
        S_wet_wing = 2 * S_wing
        C_D0_wing = C_f_wing * Ff_wing * (S_wet_wing / S_wing)

        # Horizontal Tail
        M_HT = V / math.sqrt(gamma * gas_constant * cruise_temp)
        Re_HT = (cruise_density * V * c_h_tail) / dynamic_visc
        C_f_HT = 0.455 / (
            (math.log10(Re_HT) ** 2.58) * (1 + (0.144 * M_HT**2)) ** 0.65
        )
        Ff_HT = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
            1.39 * (M_wing**0.18) * math.cos(sweep_angle) ** 0.28
        )
        S_wet_HT = 2 * S_h_tail
        C_D0_HT = C_f_HT * Ff_HT * (S_wet_HT / S_wing)

        # Vertical Tail
        M_VT = V / math.sqrt(gamma * gas_constant * cruise_temp)
        Re_VT = (cruise_density * V * c_v_tail) / dynamic_visc
        C_f_VT = 0.455 / (
            (math.log10(Re_VT) ** 2.58) * (1 + (0.144 * M_VT**2)) ** 0.65
        )
        Ff_VT = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
            1.39 * (M_VT**0.18) * math.cos(sweep_angle) ** 0.28
        )
        S_wet_VT = 2 * S_v_tail
        C_D0_VT = C_f_VT * Ff_VT * (S_wet_VT / S_wing)

        # Fuselage
        f = fuselage_length / Df
        M_fuse = V / math.sqrt(gamma * gas_constant * cruise_temp)
        Re_fuse = (cruise_density * V * fuselage_length) / dynamic_visc
        C_f_fuse = 0.455 / (
            (math.log10(Re_fuse) ** 2.58) * (1 + (0.144 * M_fuse**2)) ** 0.65
        )
        Ff_fuse = 1 + (60 / (f**3)) + (f / 400)
        S_wet_fuse = (math.pi * fuselage_length * Df) + S_wet_noseandback
        C_D0_fuse = C_f_fuse * Ff_fuse * (S_wet_fuse / S_wing)

        # AIRCRAFT
        C_D0_aircraft = C_D0_wing + C_D0_HT + C_D0_VT + C_D0_fuse
        # print("CD_0 sub: ", C_D0_aircraft)
        C_D_aircraft = C_D0_aircraft + C_D_induced
        # print("Subsonic C_D_aircraft: ", C_D_aircraft)
        D_aircraft = C_D_aircraft * q_cruise * S_wing
        # print("Aircraft drag D_a", D_aircraft, "lb")
        velocity.append(V)
        D_a.append(D_aircraft)
        thrust_cruise.append(cruise_thrust)  # cruise thrust from step 5

    # Plot drag vs. velocity
    plt.plot(velocity, D_a, color="blue", label="Subsonic Drag [lb]")
    plt.plot(velocity, thrust_cruise, color="red", label="Cruise Thrust [lb]")
    plt.title("Plot of Aircraft Drag and Thrust vs. Flight Speed")
    plt.legend()
    # plt.show()

    # Print V star
    def findIntersection(D_a, thrust_cruise):
        i = 0
        err = -1
        while err < 0:
            D = D_a[-1 - i]
            err = thrust_cruise[-1 - i] - D_a[-1 - i]
            i += 1
        # print("V*: ", velocity[-1 - i])
        return velocity[-1 - i]

    v_star = findIntersection(D_a, thrust_cruise)

    return v_star, np.round(e_0, decimals=2), np.round(V_stall, decimals=2)
