import numpy as np


def tail_sizing(
    S_wing,
    fuselage_length,
    wing_location,
    tail_end_v,
    tail_end_h,
    Y_w,
    sweep_angle_wing,
    quarter_chord_w,
    avg_chord_w,
    b_wing,
):
    sweep_angle_wing = sweep_angle_wing * np.pi / 180  # conversion to radians

    # vertical tail
    c_tip_v = 2
    c_root_v = 7
    taper_ratio_v = c_tip_v / c_root_v
    avg_chord_v = (
        (2 / 3)
        * c_root_v
        * (1 + taper_ratio_v + taper_ratio_v**2)
        / (taper_ratio_v + 1)
    )
    quarter_chord_v = avg_chord_v / 4
    sweep_angle_v = 45 * np.pi / 180  # sweep angle is 45 deg...conversion to radians
    b_v = 5  # todo: changed this value
    Y_v = 2 * (b_v * (1 + 2 * taper_ratio_v) / (6 * (1 + taper_ratio_v)))

    C_VT = 0.0605  # from Raymer
    tail_location_v = (
        tail_end_v + c_root_v
    )  # the start of the tail, in reference to the end of the plane
    wing_shift = Y_w * np.tan(sweep_angle_wing) + quarter_chord_w
    tail_shift_v = Y_v * np.tan(sweep_angle_v) + quarter_chord_v
    L_VT = fuselage_length - wing_location - tail_location_v - wing_shift + tail_shift_v
    S_v = C_VT * S_wing * b_wing / L_VT
    AR_v = b_v**2 / S_v

    # horizontal tail
    c_tip_h = 1
    c_root_h = 5
    taper_ratio_h = c_tip_h / c_root_h
    avg_chord_h = (
        (2 / 3)
        * c_root_h
        * (1 + taper_ratio_h + taper_ratio_h**2)
        / (taper_ratio_v + 1)
    )
    quarter_chord_h = avg_chord_h / 4
    b_h = 15  # todo: changed this value
    Y_h = b_h * (1 + 2 * taper_ratio_h) / (6 * (1 + taper_ratio_h))
    sweep_angle_h = 45 * np.pi / 180  # sweep angle is 45 deg...conversion to radians

    C_HT = 0.55  # from Raymer
    tail_location_h = (
        tail_end_h + c_root_h
    )  # the start of the tail, in reference to the end of the plane
    tail_shift_h = Y_h * np.tan(sweep_angle_h) + quarter_chord_h
    L_HT = fuselage_length - wing_location - tail_location_h - wing_shift + tail_shift_h
    S_h = C_HT * S_wing * avg_chord_w / L_HT
    AR_h = b_h**2 / S_h

    return np.round(
        np.array(
            [
                c_tip_v,
                c_root_v,
                avg_chord_v,
                quarter_chord_v,
                taper_ratio_v,
                b_v,
                Y_v,
                S_v,
                AR_v,
                c_tip_h,
                c_root_h,
                taper_ratio_h,
                avg_chord_h,
                quarter_chord_h,
                b_h,
                Y_h,
                S_h,
                AR_h,
            ]
        ),
        decimals=2,
    )
