import numpy as np
from scipy.optimize import fsolve



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
    taper_ratio = 0.2  # for both the horizontal and vertical tails

    # vertical tail
    class TailCharacteristics:
        def __init__(self, S_wing, b_w, Y_w, taper, sweep, b_v, b_h):
            self.S_wing = S_wing
            self.b_w = b_w
            self.Y_w = Y_w

            # tail characteristics
            self.taper_v = taper
            self.taper_h = 2 * taper
            self.sweep = sweep * np.pi / 45

            # vertical tail
            self.b_v = b_v

            # horizontal
            self.b_h = b_h

            # vertical calculated
            self.AR_v = None
            self.Y_v = None
            self.S_v = None
            self.quarter_chord_v = None
            self.avg_chord_v = None

            # horizontal calculated
            self.AR_h = None
            self.Y_h = None
            self.S_h = None
            self.quarter_chord_h = None
            self.avg_chord_h = None

        def calculate_vtail(self, c_root_v):
            self.avg_chord_v = (
                (2 / 3)
                * c_root_v
                * (1 + self.taper_v + self.taper_v**2)
                / (self.taper_v + 1)
            )
            self.quarter_chord_v = self.avg_chord_v / 4
            self.Y_v = 2 * (
                self.b_v * (1 + 2 * self.taper_v) / (6 * (1 + self.taper_v))
            )

            C_VT = 0.0605  # from Raymer
            tail_location_v = (
                tail_end_v + c_root_v
            )  # the start of the tail, in reference to the end of the plane
            wing_shift = Y_w * np.tan(sweep_angle_wing) + quarter_chord_w
            tail_shift_v = self.Y_v * np.tan(self.sweep) + self.quarter_chord_v
            L_VT = (
                fuselage_length
                - wing_location
                - tail_location_v
                - wing_shift
                + tail_shift_v
            )
            self.S_v = C_VT * S_wing * b_wing / L_VT
            self.AR_v = self.b_v**2 / self.S_v  # should be 0.6 - 1.4

            if (self.AR_v <= 1.4) & (self.AR_v >= 0.6):
                return self.b_v * self.avg_chord_v
            else:
                return 100

        def calculate_htail(self, c_root_h):
            self.avg_chord_h = (
                (2 / 3)
                * c_root_h
                * (1 + self.taper_h + self.taper_h**2)
                / (self.taper_h + 1)
            )
            self.quarter_chord_h = self.avg_chord_h / 4
            self.Y_h = self.b_h * (1 + 2 * self.taper_h) / (6 * (1 + self.taper_h))

            C_HT = 0.55  # from Raymer
            tail_location_h = (
                tail_end_h + c_root_h
            )  # the start of the tail, in reference to the end of the plane
            tail_shift_h = self.Y_h * np.tan(self.sweep) + self.quarter_chord_h
            wing_shift = self.Y_w * np.tan(self.sweep) + quarter_chord_w
            L_HT = (
                fuselage_length
                - wing_location
                - tail_location_h
                - wing_shift
                + tail_shift_h
            )
            self.S_h = C_HT * S_wing * avg_chord_w / L_HT
            self.AR_h = self.b_h**2 / self.S_h  # should be 3-4

            if (self.AR_h <= 4) & (self.AR_h >= 0):
                return self.b_h * self.avg_chord_h
            else:
                return 100

        def err_vtail(self, c_root_guess):
            S_v_calc = self.calculate_vtail(c_root_guess[0])
            error = S_v_calc - self.S_v
            return error

        def err_htail(self, c_root_guess):
            S_h_calc = self.calculate_htail(c_root_guess[0])
            error = S_h_calc - self.S_h
            return error

    b_v = 5
    b_h = 10
    tail = TailCharacteristics(
        S_wing=S_wing,
        b_w=b_wing,
        Y_w=Y_w,
        taper=taper_ratio,
        sweep=sweep_angle_wing,
        b_v=b_v,
        b_h=b_h,
    )

    c_root_vtail = fsolve(tail.err_vtail, np.array([5]))[0]
    c_tip_v = taper_ratio * c_root_vtail

    c_root_htail = fsolve(tail.err_htail, np.array([20]))[0]
    c_tip_h = taper_ratio * c_root_htail

    return np.round(
        np.array(
            [
                c_tip_v,
                c_root_vtail,
                tail.avg_chord_v,
                tail.quarter_chord_v,
                tail.taper_v,
                b_v,
                tail.Y_v,
                tail.S_v,
                tail.AR_v,
                c_tip_h,
                c_root_htail,
                tail.taper_h,
                tail.avg_chord_h,
                tail.quarter_chord_h,
                tail.b_h,
                tail.Y_h,
                tail.S_h,
                tail.AR_h,
            ]
        ),
        decimals=2,
    )
