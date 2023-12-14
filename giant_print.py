def final_characteristics(
    R_sub,
    R_super,
    cruise_alt,
    SFC,
    SFC_super,
    V_c,
    M_super,
    com,
    loiter,
    payload,
    num_crew,
    takeoff_weight,
    empty_weight,
    e_0,
    V_stall,
    AR_wing,
    b_w,
    S_w,
    taper_ratio_w,
    sweep_angle,
    root_chord,
    tip_chord,
    avg_chord,
    quarter_chord,
    AR_h,
    b_h,
    S_h,
    taper_ratio_h,
    c_root_h,
    c_tip_h,
    c_avg_h,
    quarter_c_h,
    AR_v,
    b_v,
    S_v,
    taper_ratio_v,
    c_root_v,
    c_tip_v,
    c_avg_v,
    quarter_c_v,
    fuse_length,
    fuse_diameter,
    w_loading_cruise,
    w_loading_takeoff,
    w_loading_supersonic,
    w_loading_loiter,
    w_loading_landing,
    thrust_weight_cruise,
    thrust_weight_takeoff,
    thrust_weight_loiter,
    thrust_weight_supersonic,
    thrust_weight_landing,
    cruise_thrust,
    thrust_supersonic,
    loiter_thrust,
    thrust_takeoff,
    thrust_landing,
    x_cg,
    x_np,
    static_margin,
    thrust_weight_climb,
    climb_thrust,
):
    print("DESIGN SPECIFICATIONS:")
    print("The subsonic range is: ", R_sub, "mi")
    print("The cruise velocity is: ", V_c, "mph")
    print("The subsonic SFC is: ", SFC, "1/hr")
    print("The cruise altitude is: ", cruise_alt, "ft")
    print("The supersonic range is: ", R_super, "mi")
    print("The supersonc Mach number is: ", M_super)
    print("The supersonic SFC is: ", SFC_super, "1/hr")
    print("The combat endurance is: ", com, "hr")
    print("The combat SFC is: ", SFC, "1/hr")
    print("The loiter endurance is: ", loiter, "hr")
    print("The loiter SFC is: ", SFC, "1/hr")
    print("The payload is: ", payload, "lbf")
    print("The number of crew members is: ", num_crew)

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("CALCULATED PERFORMANCE")
    print("The takeoff weight is: ", takeoff_weight, "lbf")
    print("The empty weight is: ", empty_weight, "lbf")
    print("The efficiency factor is: ", e_0)
    print("The stall speed is: ", V_stall, "ft/s")

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("WING PARAMETERS")
    print("The aspect ratio is: ", AR_wing)
    print("The wingspan is: ", b_w, "ft")
    print("The wing area is: ", S_w, "ft^2")
    print("The taper ratio is: ", taper_ratio_w)
    print("Sweep angle is: ", sweep_angle, "deg")
    print("The root chord is: ", root_chord, "ft")
    print("The tip chord is: ", tip_chord, "ft")
    print("The average chord is: ", avg_chord, "ft")
    print("The quarter chord length is: ", quarter_chord, "ft")

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("TAIL PARAMETERS")
    print("Horizontal Tail")
    print("The aspect ratio is: ", AR_h)
    print("The wingspan is: ", b_h, "ft")
    print("The wing area is: ", S_h, "ft^2")
    print("The taper ratio is: ", taper_ratio_h)
    print("Sweep angle is: ", sweep_angle)
    print("The root chord is: ", c_root_h, "ft")
    print("The tip chord is: ", c_tip_h, "ft")
    print("The average chord is: ", c_avg_h, "ft")
    print("The quarter chord length is: ", quarter_c_h, "ft")

    print("Vertical Tail")
    print("The aspect ratio is: ", AR_v)
    print("The wingspan is: ", b_v, "ft")
    print("The wing area is: ", S_v, "ft^2")
    print("The taper ratio is: ", taper_ratio_v)
    print("Sweep angle is: ", sweep_angle, "deg")
    print("The root chord is: ", c_root_v, "ft")
    print("The tip chord is: ", c_tip_v, "ft")
    print("The average chord is: ", c_avg_v, "ft")
    print("The quarter chord length is: ", quarter_c_v, "ft")

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("FUSELAGE")
    print("The length is: ", fuse_length, "ft")
    print("The diameter is: ", fuse_diameter, "ft")

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("WING LOADING")
    print("The wing loading at cruise is: ", w_loading_cruise, "lbf/ft^2")
    print("The wing loading at loiter is: ", w_loading_loiter, "lbf/ft^2")
    print("The wing loading at supersonic dash is: ", w_loading_supersonic, "lbf/ft^2")
    print("The wing loading at takeoff is: ", w_loading_takeoff, "lbf/ft^2")
    print("The wing loading at landing is: ", w_loading_landing)

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("THRUST TO WEIGHT")
    print("The thrust to weight ratio at cruise is: ", thrust_weight_cruise)
    print("The thrust to weight ratio at loiter is: ", thrust_weight_loiter)
    print(
        "The thrust to weight ratio at supersonic dash is: ", thrust_weight_supersonic
    )
    print("The thrust to weight ratio at takeoff is: ", thrust_weight_takeoff)
    print("The thrust to weight ratio at landing is: ", thrust_weight_landing)

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("REQUIRED THRUST")
    print("The required thrust at cruise is: ", cruise_thrust)
    print("The required thrust at loiter is: ", loiter_thrust)
    print("The required thrust at supersonic dash is: ", thrust_supersonic)
    print("The required thrust at takeoff is: ", thrust_takeoff)
    print("The required thrust at landing is: ", thrust_landing)

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("STABILITY")
    print("The center of mass is: ", x_cg, "ft from front of the plane")
    print("The neutral point is: ", x_np, "ft from front of the plane")
    print("The static margin is: ", static_margin)

    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print("MANEUVER ANALYSIS")
    print("The thrust to weight ratio at climb is: ", thrust_weight_climb)
    print("The required thrust at climb point is: ", climb_thrust, "lbf")
