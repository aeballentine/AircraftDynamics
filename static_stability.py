import numpy as np


def pitch_stability(
    S_v_tail, S_h_tail, S_wing, S_fuselage, takeoff_weight, engine_weight
):
    v_tail_weight = 5.3 * S_v_tail
    h_tail_weight = 4 * S_h_tail
    wing_weight = 9 * S_wing
    fuselage_weight = 4.8 * S_fuselage

    landing_weight = 0.033 * takeoff_weight
    engine_weight = 1.3 * engine_weight
    all_else_weight = 0.17 * takeoff_weight

    wing_location = 0.4 * avg_chord + wing_location
