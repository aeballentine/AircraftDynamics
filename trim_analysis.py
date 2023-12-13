import numpy as np


def trim_analysis(
    M_subsonic, Cl_alpha, S_wing, fuselage_diameter, c_root, b_w, AR_wing, sweep_angle
):
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
    CL_total = CL_alpha_wing * (alpha + i_w) + eta_h * CL_h * S_h / S_wing
