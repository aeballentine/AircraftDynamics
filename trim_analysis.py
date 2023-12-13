import numpy as np


def trim_analysis(
    M_subsonic, Cl_alpha, S_wing, fuselage_diameter, c_root, b_w, AR_wing, sweep_angle,
        x_cg, w_cruise, cruise_density, V_c,
):
    beta = np.sqrt(1 - M_subsonic**2)
    eta = Cl_alpha / (2 * np.pi / beta)
    eta_h = CL_alpha_HT / (2 * np.pi / beta) # todo - check this
    S_exposed = S_wing - fuselage_diameter * c_root
    d = fuselage_diameter
    F = 1.07 * (1 + d / b_w) ** 2
    alpha_wing_L0 = -2.5*(np.pi/180) # Wing AOA at zero lift in radians
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
    CM_G = []
    CL_total = []
    for alpha_wing in range((-2*(np.pi/180)),(8*(np.pi/180))):
        ih = 0
        CL_alpha_HT =
        alpha_L0_HT =  # HT AOA at zero lift
        CL_wing = CL_alpha_wing * (alpha_wing - alpha_wing_L0)
        CL_HT = CL_alpha_HT * ((alpha_wing * WT) + ih - alpha_L0_HT)
        CM_G_iteration = CL_wing * (x_cg - x_ac_w) + CM_w_ac - (eta_HT * (S_HT / S_wing) * CL_HT * (x_ac_HT - x_cg))
        CL_total_iteration = CL_alpha_wing * (alpha + i_w) + eta_h * CL_h * S_h / S_wing
        CM_G.append(CM_G_iteration)
        CL_total.append(CL_total_iteration)

        # Plot
        plt.plot(CL_total, CM_G)
        plt.title("Moment Coefficient about Center of Gravity vs Total Lift Coefficent")
        plt.legend()
        plt.show()

    # Find trim pt
    def findTrimPt(CL_total, CM_G):
    i = 0
    err = -1
    while err < 0:
        total_lift_co = CL_total[-1 - i]
        err = CM_G[-1 - i] - CL_total[-1 - i]
        i += 1
    # print("V*: ", velocity[-1 - i])
    return CL_total[-1 - i]

    CL_trim_pt = findTrimPt(CL_total, CM_G)

    return CL_trim_pt

    error = CL_trim_pt - (w_cruise / (0.5 * cruise_density * (V_C**2) * S_wing))
    print("Total CL at trim point: ", CL_trim_pt)
    print("Error: ", error)

