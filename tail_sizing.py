import numpy as np


def tail_sizing(S_wing):
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
    b_v = 3
    Y_v = 2 * (b_v * (1 + 2 * taper_ratio_v) / (6 * (1 + taper_ratio_v)))
    C_VT = 0.06  # todo: check this value
    L_VT = 22  # todo: figure out how to do this
    S_v = C_VT * S_wing * avg_chord_v / L_VT
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
    b_h = 12
    Y_h = b_h * (1 + 2 * taper_ratio_h) / (6 * (1 + taper_ratio_h))
    C_HT = 0.5  # todo: check this value
    L_HT = 16  # todo: figure out how to do this
    S_h = C_HT * S_wing * avg_chord_h / L_HT
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
