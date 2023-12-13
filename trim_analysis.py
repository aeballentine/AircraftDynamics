import numpy as np
import matplotlib.pyplot as plt


def trim_analysis(
    M_subsonic,
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
    wing_location,
    Y_wing,
    avg_chord,
    quarter_chord,
    quarter_c_h,
    fuselage_length,
    h_tail_end,
    Y_h_tail,
    c_h_tail,
    Cm_airfoil,
    tc,
):
    alpha_list = []
    CL_list = []
    Cm_list = []
    sweep_angle = sweep_angle * np.pi / 180  # conversion to radians
    for alpha in (np.pi / 180) * np.array([-3, -2, -1, 0, 1, 2, 3]):
        for i_h in (np.pi / 180) * np.array([-10, 0, 10]):
            alpha_list.append(alpha)
            beta = np.sqrt(1 - M_subsonic**2)
            eta = Cl_alpha / (2 * np.pi / beta)
            S_wet = S_wing - fuselage_diameter * c_root
            S_exposed = S_wet / (1.977 + (0.52*tc))
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
            i_w = 0
            n_h = 0.9  # assuming that the tail is fully out of the prop wash, Raymer pg. 606

            S_exposed_h = (
                S_h_tail - 0.25 * fuselage_diameter * c_root_h
            )  # todo: check the 0.25 value
            eta_h = Cl_alpha_h / (2 * np.pi / beta)
            CL_alpha_h = (
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
            x_cg_wing = wing_location + Y_wing * np.tan(sweep_angle) + avg_chord * 0.4
            x_cg_h = (
                fuselage_length
                - h_tail_end
                - c_root_h
                + Y_h_tail * np.tan(sweep_angle)
                + 0.4 * c_h_tail
            )

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

            CL_wing = CL_alpha_wing * alpha
            CL_h = CL_alpha_h * (alpha + i_w)

            Cm_wing = Cm_airfoil * (
                AR_wing * np.cos(sweep_angle) ** 2 / (AR_wing + 2 * np.cos(sweep_angle))
            )

            Cm_CG = (
                CL_wing * (x_cg_wing - x_ac_wing)
                + Cm_wing
                - n_h * (S_h_tail / S_wing) * CL_h * (x_ac_h - x_cg_h)
            )
            CL_h = CL_alpha_h * (alpha + i_h)
            CL_total = CL_alpha_wing * (alpha + i_w) + n_h * CL_h * S_h_tail / S_wing

            CL_list.append(CL_total)
            Cm_list.append(Cm_CG)

    plt.plot(CL_list[0:2], Cm_list[0:2], color="black")
    plt.plot(CL_list[3:5], Cm_list[3:5], color="blue")
    plt.plot(CL_list[6:8], Cm_list[6:8], color="purple")

    plt.plot(CL_list[9:11], Cm_list[9:11], color="green")
    plt.plot(CL_list[12:14], Cm_list[12:14], color="orange")
    plt.plot(CL_list[15:17], Cm_list[15:17], color="red")
    plt.plot(CL_list[18:20], Cm_list[18:20], color="yellow")

    plt.legend(
        [
            "Alpha = -3",
            "Alpha = -2",
            "Alpha = -1",
            "Alpha = 0",
            "Alpha = 1",
            "Alpha = 2",
            "Alpha = 3",
        ]
    )
    plt.xlabel("Coefficient of Lift")
    plt.ylabel("Coefficient of Moment")

    # plt.xlim([-1, 1])
    # plt.ylim([-0.1, 0.1])

    plt.show()
