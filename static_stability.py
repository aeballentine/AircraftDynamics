import numpy as np

# todo: will need to include this analysis for supersonic leg as well


def center_of_gravity(
    S_v_tail,
    S_h_tail,
    S_wing,
    S_fuselage,
    takeoff_weight,
    engine_weight,
    avg_chord,
    wing_location,
    fuselage_length,
    h_tail_end,
    c_root_h,
    c_h_tail,
    v_tail_end,
    c_root_v,
    c_v_tail,
    w_fuel,
    fuel_location,
    landing_location,
    engine_location,
    Y_wing,
    sweep_angle,
    Y_h_tail,
    Y_v_tail,
):
    v_tail_weight = 5.3 * S_v_tail
    h_tail_weight = 4 * S_h_tail
    wing_weight = 9 * S_wing
    fuselage_weight = 4.8 * S_fuselage

    landing_weight = 0.033 * takeoff_weight
    engine_weight = 1.3 * engine_weight  # todo: one or two engines?
    all_else_weight = 0.17 * takeoff_weight
    fuel_weight = w_fuel

    wing_location = wing_location + Y_wing * np.tan(sweep_angle) + avg_chord * 0.4
    h_tail_location = (
        fuselage_length
        - h_tail_end
        - c_root_h
        + Y_h_tail * np.tan(sweep_angle)
        + 0.4 * c_h_tail
    )
    v_tail_location = (
        fuselage_length
        - v_tail_end
        - c_root_v
        + Y_v_tail * np.tan(sweep_angle)
        + 0.4 * c_v_tail
    )
    fuselage_location = 0.4 * fuselage_length  # can also be 0.5 if needed

    landing_location = landing_location * fuselage_length
    engine_location = engine_location * fuselage_length
    all_else_location = 0.4 * fuselage_length
    fuel_location = fuel_location  # * fuselage_length

    summation = (
        v_tail_weight * v_tail_location
        + wing_weight * wing_location
        + h_tail_weight * h_tail_location
        + fuselage_weight * fuselage_location
        + 0.85 * landing_weight * landing_location
        + 0.15 * landing_weight * 1
        + engine_weight * engine_location
        + all_else_weight * all_else_location
        + fuel_weight * fuel_location
    )
    x_cg = summation / (
        v_tail_weight
        + h_tail_weight
        + wing_weight
        + fuselage_weight
        + landing_weight
        + engine_weight
        + all_else_weight
        + fuel_weight
    )

    weights_buildup = dict(
        {
            "Vertical tail location, weight": np.round(
                np.array([v_tail_location, v_tail_weight]), decimals=2
            ),
            "Horizontal tail location, weight": np.round(
                np.array([h_tail_location, h_tail_weight]), decimals=2
            ),
            "Wing location, weight": np.round(
                np.array([wing_location, wing_weight]), decimals=2
            ),
            "Landing gear location front, weight": np.round(
                np.array([1, 0.15 * landing_weight]), decimals=2
            ),
            "Landing gear location back, weight": np.round(
                np.array([landing_location, 0.85 * landing_weight]), decimals=2
            ),
            "Fuselage location, weight": np.round(
                np.array([fuselage_location, fuselage_weight]), decimals=2
            ),
            "Engine location, weight": np.round(
                np.array([engine_location, engine_weight]), decimals=2
            ),
            "Fuel location, weight": np.round(
                np.array([fuel_location, fuel_weight]), decimals=2
            ),
            "All else location, weight": np.round(
                np.array([all_else_location, all_else_weight]), decimals=2
            ),
            "Total weight": np.round(
                wing_weight
                + v_tail_weight
                + h_tail_weight
                + fuselage_weight
                + landing_weight
                + engine_weight
                + fuel_weight
                + all_else_weight
            ),
            "Center of gravity location": np.round(x_cg, decimals=2),
        }
    )

    return [np.round(x_cg, decimals=2), weights_buildup]


# subsonic neutral point:
def neutral_point(
    quarter_chord,
    avg_chord,
    S_wing,
    M_subsonic,
    quarter_c_h,
    S_h_tail,
    Cl_alpha,
    AR_wing,
    sweep_angle,
    fuselage_diameter,
    fuselage_length,
    fuselage_weight,
    c_root,
    b_w,
    c_root_h,
    AR_h_tail,
    Cl_alpha_h,
    wing_location,
    Y_wing,
    h_tail_end,
    Y_h_tail,
):
    sweep_angle = sweep_angle * np.pi / 180

    # shift in aerodynamic center as Mach number increases (transsonic):
    delta_xac = 0.26 * (M_subsonic - 0.4) ** 2.5
    x_ac_wing = quarter_chord + delta_xac * np.sqrt(S_wing)
    x_ac_h = quarter_c_h + delta_xac * np.sqrt(S_h_tail)
    x_ac_wing = wing_location + Y_wing * np.tan(sweep_angle) + x_ac_wing
    x_ac_h = (
        fuselage_length
        - h_tail_end
        - c_root_h
        + Y_h_tail * np.tan(sweep_angle)
        + x_ac_h
    )

    # lift curve slopes (pg. 400)
    beta = np.sqrt(1 - M_subsonic**2)
    eta = Cl_alpha / (2 * np.pi / beta)
    S_exposed = S_wing - fuselage_diameter * c_root
    d = fuselage_diameter
    F = 1.07 * (1 + d / b_w) ** 2
    CL_alpha_wing = (
        2
        * np.pi
        * AR_wing
        * (S_exposed / S_wing)
        * F
        / (
            2
            + np.sqrt(
                4
                + (AR_wing * beta / eta) ** 2
                * (1 + np.tan(sweep_angle) ** 2 / beta**2)
            )
        )
    )

    eta_h = Cl_alpha_h / (2 * np.pi / beta)
    S_exposed_h = (
        S_h_tail - 0.2 * fuselage_diameter * c_root_h
    )  # todo: check the 0.25 value
    CL_alpha_h_tail = (
        2
        * np.pi
        * AR_wing
        * (S_exposed_h / S_h_tail)
        / (
            2
            + np.sqrt(
                4
                + (AR_h_tail * beta / eta_h) ** 2
                * (1 + np.tan(sweep_angle) ** 2 / beta**2)
            )
        )
    )

    n_h = 0.9  # assuming that the tail is fully out of the prop wash, Raymer pg. 606

    de_da = 1.62 * CL_alpha_wing / (np.pi * AR_wing)
    da_h_da = 1 - de_da

    x_np = (
        CL_alpha_wing * x_ac_wing
        + n_h * (S_h_tail / S_wing) * CL_alpha_h_tail * da_h_da * x_ac_h
    ) / (CL_alpha_wing + n_h * (S_h_tail / S_wing) * CL_alpha_h_tail * da_h_da)

    return np.round(x_np, decimals=2)


def neutral_point_super(
    quarter_chord,
    S_wing,
    M_super,
    quarter_c_h,
    S_h_tail,
    AR_wing,
    sweep_angle,
    fuselage_length,
    c_root_h,
    wing_location,
    Y_wing,
    h_tail_end,
    Y_h_tail,
    avg_chord,
    avg_chord_h,
):
    sweep_angle = sweep_angle * np.pi / 180

    # shift in aerodynamic center as Mach number increases (transsonic):
    delta_xac = 0.112 - 0.004 * M_super

    x_ac_wing = quarter_chord + delta_xac * np.sqrt(S_wing)
    x_ac_h = quarter_c_h + delta_xac * np.sqrt(S_h_tail)
    x_ac_wing = wing_location + Y_wing * np.tan(sweep_angle) + x_ac_wing
    x_ac_h = (
        fuselage_length
        - h_tail_end
        - c_root_h
        + Y_h_tail * np.tan(sweep_angle)
        + x_ac_h
    )

    # lift curve slopes (pg. 400)
    beta = np.sqrt(M_super**2 - 1)
    CL_alpha_wing = 4 / beta
    CL_alpha_h_tail = CL_alpha_wing

    n_h = 0.9  # assuming that the tail is fully out of the prop wash, Raymer pg. 606

    de_da = 1.62 * CL_alpha_wing / (np.pi * AR_wing)
    da_h_da = 1 - de_da

    x_np = (
        CL_alpha_wing * x_ac_wing
        + n_h * (S_h_tail / S_wing) * CL_alpha_h_tail * da_h_da * x_ac_h
    ) / (CL_alpha_wing + n_h * (S_h_tail / S_wing) * CL_alpha_h_tail * da_h_da)
    print("Neutral point: ", x_np)
    return np.round(x_np, decimals=2)
