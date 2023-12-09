from scipy.optimize import fsolve
import numpy as np


class PitchStability:
    def __init__(
        self,
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
    ):
        self.v_tail_weight = 5.3 * S_v_tail
        self.h_tail_weight = 4 * S_h_tail
        self.wing_weight = 9 * S_wing
        self.fuselage_weight = 4.8 * S_fuselage

        self.landing_weight = 0.033 * takeoff_weight
        self.engine_weight = 1.3 * engine_weight
        self.all_else_weight = 0.17 * takeoff_weight
        self.fuel_weight = w_fuel

        self.wing_location = 0.4 * avg_chord + wing_location
        self.h_tail_location = fuselage_length - h_tail_end - c_root_h + 0.4 * c_h_tail
        self.v_tail_location = fuselage_length - v_tail_end - c_root_v + 0.4 * c_v_tail
        self.fuselage_location = 0.4 * fuselage_length  # can also be 0.4 if needed
        self.all_else_location = 0.5 * fuselage_length
        self.fuel_location = fuel_location * fuselage_length

        self.centroid = None

    def find_centriod(self, centroid_guess):
        summation = (
            self.v_tail_weight * self.v_tail_location
            + self.wing_weight * self.wing_location
            + self.h_tail_weight * self.h_tail_location
            + self.fuselage_weight * self.fuselage_location
            + 0.85 * self.landing_weight * centroid_guess
            + 0.15 * self.landing_weight * 1
            + self.engine_weight * centroid_guess
            + self.all_else_weight * self.all_else_location
            + self.fuel_weight * self.fuel_location
        )
        centroid_actual = summation / (
            self.v_tail_weight
            + self.h_tail_weight
            + self.wing_weight
            + self.fuselage_weight
            + self.landing_weight
            + self.engine_weight
            + self.all_else_weight
        )

        return centroid_actual - centroid_guess

    def centroid_location(self):
        self.centroid = np.round(
            fsolve(self.find_centriod, np.array([12]))[0], decimals=2
        )
