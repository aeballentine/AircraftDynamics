import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# NOTE - update cruise weight after refined estimate
# todo: supersonic wave drag


def super_propulsion_analysis(
    c_l_max,
    w_landing,
    cruise_density,
    S_wing,
    V_c,
    AR_wing,
    w_cruise,
    cruise_temp,
    xc_max,
    tc,
    sweep_angle,
    c_h_tail,
    c_v_tail,
    S_h_tail,
    S_v_tail,
    fuselage_length,
    dynamic_visc,
    M_super,
    thrust_supersonic,
    avg_chord,
    takeoff_weight,
    Re_wing,
    M_subsonic,
    cruise_thrust,

):
    # Define stall speed and cruise speed, conditions
    V_stall = round(
        math.sqrt(2 * w_landing / (cruise_density * S_wing * c_l_max))
    )  # ft/s
    V_c_ft = round(V_c / 0.682)  # ft/s
    # b_w = 29.5
    e_0 = 1.78 * (1 - (0.045 * AR_wing**0.68)) - 0.64  # Refined e_0
    gamma = 1.4
    gas_constant = 1716  # ft-lbf/slug-R
    sweep_angle = sweep_angle * np.pi / 180  # conversion to radians
    fineness_ratio = 12  # based on pg 157
    Df = fuselage_length / fineness_ratio  # fuselage diameter - FIX
    A_max = math.pi*(Df/2)**2 #max cross sectional area of aircraft (eqn 12.44)
    h_nose = Df
    S_wet_noseandback = 2 * math.pi * (Df / 2) * math.sqrt((Df / 2) ** 2 + h_nose**2)
    V_super = M_super*math.sqrt(gamma*gas_constant*cruise_temp)

    # Solve for velocity range
    super_velocity = []
    D_super = []
    thrust_super = []
    for V in range(V_stall, round(1.2 * V_super) + 1):
        q_super = 0.5 * cruise_density * (V**2)
        C_L_aircraft = w_cruise / (q_super * S_wing)
        C_D_induced = (C_L_aircraft**2) / (math.pi * AR_wing * e_0)
        # print('CD induced: ', C_D_induced)

        # Wing
        M_wing = M_super  # todo: do we need to multiply this by the sweep angle?
        Re_wing = (cruise_density * V_super * avg_chord) / dynamic_visc
        C_f_wing = 0.455 / (
            (math.log10(Re_wing) ** 2.58) * (1 + (0.144 * M_wing**2)) ** 0.65
        )
        Ff_wing = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
            1.39 * (M_wing**0.18) * math.cos(sweep_angle) ** 0.28
        )
        S_wet_wing = 2 * S_wing
        C_D0_wing = C_f_wing * Ff_wing * (S_wet_wing / S_wing)

        # Horizontal Tail
        M_HT = V_super / math.sqrt(gamma * gas_constant * cruise_temp)
        Re_HT = (cruise_density * V_super * c_h_tail) / dynamic_visc
        C_f_HT = 0.455 / (
            (math.log10(Re_HT) ** 2.58) * (1 + (0.144 * M_HT**2)) ** 0.65
        )
        Ff_HT = (1 + ((0.6 / xc_max) * tc) + (tc**4)) * (
            1.39 * (M_HT**0.18) * math.cos(sweep_angle) ** 0.28
        )
        S_wet_HT = 2 * S_h_tail
        C_D0_HT = C_f_HT * Ff_HT * (S_wet_HT / S_wing)

        # Vertical Tail
        M_VT = V_super / math.sqrt(gamma * gas_constant * cruise_temp)
        Re_VT = (cruise_density * V_super * c_v_tail) / dynamic_visc
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
        M_fuse = V_super / math.sqrt(gamma * gas_constant * cruise_temp)
        Re_fuse = (cruise_density * V_super * fuselage_length) / dynamic_visc
        C_f_fuse = 0.455 / (
            (math.log10(Re_fuse) ** 2.58) * (1 + (0.144 * M_fuse**2)) ** 0.65
        )
        Ff_fuse = 1 + (60 / (f**3)) + (f / 400)
        S_wet_fuse = (math.pi * fuselage_length * Df) + S_wet_noseandback
        C_D0_fuse = C_f_fuse * Ff_fuse * (S_wet_fuse / S_wing)

        # Wave drag
        Dq_ratio_sears_hack = (((9*math.pi)/2)*(A_max/fuselage_length)**2) #Raymer eqn 12.44
        Ewd = 2 # spec based on eqn 12.45 and subsequent text
        Dq_ratio_wave = Dq_ratio_sears_hack*Ewd*(1-((0.386*(M_super-1.2)**0.57)*(1-((math.pi*sweep_angle**0.77)/100))))
        C_D0_wave = Dq_ratio_wave / S_wing

        # AIRCRAFT
        C_D0_super = C_D0_wing + C_D0_HT + C_D0_VT + C_D0_fuse + C_D0_wave
        #print("CD_0 super: ", C_D0_super)
        C_D_super = C_D0_super + C_D_induced
        #print("C_D_super: ", C_D_super)
        D_aircraft = C_D_super * q_super * S_wing
        super_velocity.append(V)
        D_super.append(D_aircraft)
        thrust_super.append(thrust_supersonic)  # cruise thrust from step 5

        # If statement below used to find supersonic drag at supersonic V, then used to adjust
        # supersonic thrust accordingly - more on this in report
        # Supersonic thrust = 1210.91
        if V == 1210:
            print("Drag at supersonic V: ", D_aircraft)
        else:
            pass



    #print("Supersonic thrust: ",thrust_supersonic)
    #print("Supersonic drag: ",D_super)
    # Plot drag vs. velocity
    plt.plot(super_velocity, D_super, color="green", label="Supersonic Drag [lb]")
    plt.plot(super_velocity, thrust_super, color="orange", label="Supersonic Thrust [lb]")
    plt.title("Plot of Aircraft Drag and Thrust vs. Flight Speed")
    plt.legend()
    plt.show()

    #print("supersonic drag at supersonic M: ", D_super(1210))
    # Print V star supersonic
    def findIntersection(D_super, thrust_super):
        i = 0
        err = -1
        while err < 0:
            D = D_super[-1 - i]
            err = thrust_super[-1 - i] - D_super[-1 - i]
            i += 1
        # print("V*: ", velocity[-1 - i])
        return super_velocity[-1 - i]

    v_star_super = findIntersection(D_super, thrust_super)

    return v_star_super
