import math

def man_analysis(
    M_subsonic,
    V_c,
    Cl_alpha,
    S_wing,
    fuselage_diameter,
    c_root,
    b_w,
    AR_wing,
    sweep_angle,
    c_root_h,
    S_h_tail,
    AR_h_tail,
    Cl_alpha_h,
    S_h,
    alpha,
    wing_location,
    Y_wing,
    avg_chord,
    quarter_chord,
    quarter_c_h,
    fuselage_length,
    h_tail_end,
    Y_h_tail,
    c_h_tail,
    V_stall,
    thrust_weight_TO,
    W_climb,
    g,
):
    # Climb T/W
    lift_drag_TO = (thrust_weight_TO)**(-1)
    V_TO = 1.2 * V_stall
    #V_v = V_TO * math.sin(climb_angle)
    V_v = 50 #from lecture 26 in ft/s
    thrust_weight_climb = (V_v/V_TO) + (1/lift_drag_TO)
    print("Trust-to-weight ratio at climb: ", thrust_weight_climb)
    thrust_climb = thrust_weight_climb * W_climb
    print("Thrust at climb: ", thrust_climb)

    # Level turn analysis: turn rate, turn radius
    load_factor =
    turn_rate = (g*math.sqrt(load_factor**2-1))/V_TO
    turn_radius = (V_TO**2)/(g*math.sqrt(load_factor**2-1))

