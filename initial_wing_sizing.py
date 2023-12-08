import numpy as np


def initial_wing_sizing(W0, M_subsonic):
    # span and aspect ratio calculations
    S_new = (
        W0 / 60
    )  # guessing based on values between typical jet trainer and jet fighter
    a = 4.11
    c = -0.622
    AR_new = a * M_subsonic**c
    b_new = np.sqrt(AR_new * S_new)

    # new sweep angle
    sweep_angle = 45  # in deg, assuming that maximum Mach is 1.25

    # chord calculations
    c_tip = 3
    c_root = 12.5
    taper_ratio = (
        0.45  # using Raymer, elliptical lift distribution, and the sweep angle
    )
    avg_chord = (
        (2 / 3) * c_root * (1 + taper_ratio + taper_ratio**2) / (taper_ratio + 1)
    )
    c_root_new = 2 * S_new / (b_new * (1 + taper_ratio))
    c_tip_new = taper_ratio * c_root
    quarter_chord = avg_chord / 4

    # aerodynamic center to the mean chord
    Y = b_new * (1 + 2 * taper_ratio) / (6 * (1 + taper_ratio))

    return np.round(
        np.array(
            [
                S_new,
                b_new,
                AR_new,
                avg_chord,
                sweep_angle,
                c_tip_new,
                c_root_new,
                quarter_chord,
                Y,
            ]
        ),
        decimals=2,
    )
