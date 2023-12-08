import math
import numpy as np


def wing_loading(
    W0,
    cruise_density,
    loiter_density,
    temp_cruise,
    V_c,
    M_super,
    e_0,
    b_w,
    S_w,
    takeoff_weight,
    w_cruise,
    w_loiter,
    w_supersonic,
    w_landing,
    c_l_max,
):
    # W0 in lbf, density in slug/ft^3, velocities in mph, areas/lengths in ft

    # constants:
    gamma = 1.4
    gas_constant = 1716  # in ft-lbf/slug-R

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WING LOADING - CRUISE
    # dynamic pressure at cruise
    V_c_ft = V_c / 0.682  # conversion to ft/s
    q_c = 0.5 * cruise_density * V_c_ft**2

    # wing dimensions
    AR_w = b_w**2 / S_w

    # wing loading at cruise
    C_D0 = 0.015
    wing_loading_cruise_uncorr = q_c * math.sqrt((C_D0 * math.pi * AR_w * e_0) / 3)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WING LOADING - LOITER / COMBAT
    # dynamic pressure at loiter
    V_loiter = 338  # speed in ft/s, =200 knots
    q_l = 0.5 * loiter_density * V_loiter**2

    # wing loading at loiter
    wing_loading_loiter_uncorr = q_l * math.sqrt(C_D0 * math.pi * AR_w * e_0)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WING LOADING - LANDING
    density_SL = 0.00238  # density at SL in slug/ft^3
    V_stall = math.sqrt(2 * w_landing / (density_SL * S_w * c_l_max))
    q_landing = 0.5 * density_SL * V_stall**2

    # wing loading
    wing_loading_landing_uncorr = c_l_max * q_landing

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WING LOADING - TAKEOFF
    density_airport = density_SL
    TOP = 160  # based on S_g (2500 ft) and Fig. 5.4
    sigma = density_airport / density_SL
    C_LTO = c_l_max

    thrust_weight_TO = 0.488 * M_super**0.728  # table 5.3
    wing_loading_TO_uncorr = TOP * sigma * C_LTO * thrust_weight_TO

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WING LOADING - SUPERSONIC
    V_super = M_super * np.sqrt(gamma * gas_constant * temp_cruise)  # in ft/s
    q_super = 0.5 * cruise_density * V_super**2
    wing_loading_supersonic_uncorr = q_super * math.sqrt(
        (C_D0 * math.pi * AR_w * e_0) / 3
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CORRECTED WING LOADINGS
    wing_loading_cruise_corr = wing_loading_cruise_uncorr * (W0 / w_cruise)
    wing_loading_loiter_corr = wing_loading_loiter_uncorr * (W0 / w_loiter)
    wing_loading_landing_corr = wing_loading_landing_uncorr * (W0 / w_landing)
    wing_loading_TO_corr = wing_loading_TO_uncorr
    wing_loading_supersonic_corr = wing_loading_supersonic_uncorr * (W0 / w_supersonic)

    wing_loading_uncorrected = np.array(
        [
            wing_loading_TO_uncorr,
            wing_loading_cruise_uncorr,
            wing_loading_supersonic_uncorr,
            wing_loading_loiter_uncorr,
            wing_loading_landing_uncorr,
        ]
    )

    wing_loading_corrected = np.array(
        [
            wing_loading_TO_corr,
            wing_loading_cruise_corr,
            wing_loading_supersonic_corr,
            wing_loading_loiter_corr,
            wing_loading_landing_corr,
        ]
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # REFINED WING AREA
    Sw_TO = takeoff_weight / wing_loading_TO_corr
    Sw_cruise = w_cruise / wing_loading_cruise_corr
    Sw_landing = w_landing / wing_loading_landing_corr
    Sw_loiter = w_loiter / wing_loading_loiter_corr
    wing_areas = np.array([Sw_TO, Sw_cruise, Sw_landing, Sw_loiter])
    # Sw_refined = refined wing loading is the maximum of the wing areas

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # THRUST-WEIGHT RATIO - CRUISE
    thrust_weight_cruise = ((q_c * C_D0) / wing_loading_cruise_uncorr) + (
        wing_loading_cruise_uncorr / (math.pi * AR_w * e_0 * q_c)
    )
    thrust_cruise = thrust_weight_cruise * w_cruise

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # THRUST-WEIGHT RATIO - LOITER
    thrust_weight_loiter = ((q_l * C_D0) / wing_loading_loiter_uncorr) + (
        wing_loading_loiter_uncorr / (math.pi * q_l * AR_w * e_0)
    )
    thrust_loiter = thrust_weight_loiter * w_loiter

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # THRUST-WEIGHT RATIO - TAKEOFF
    thrust_TO = thrust_weight_TO * takeoff_weight

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # THRUST-WEIGHT RATIO - LANDING
    thrust_weight_landing = ((q_landing * C_D0) / wing_loading_landing_uncorr) + (
        wing_loading_landing_uncorr / (math.pi * q_landing * AR_w * e_0)
    )
    thrust_landing = thrust_weight_landing * w_landing

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # THRUST-WEIGHT RATIO - COMBAT/SUPERSONIC
    thrust_weight_supersonic = 0.514 * M_super**0.141
    thrust_supersonic = thrust_weight_supersonic * w_supersonic

    thrust_to_weight = np.array(
        [
            thrust_weight_TO,
            thrust_weight_cruise,
            thrust_weight_supersonic,
            thrust_weight_loiter,
            thrust_weight_landing,
        ]
    )
    thrust = np.array(
        [
            thrust_TO,
            thrust_cruise,
            thrust_supersonic,
            thrust_loiter,
            thrust_landing,
        ]
    )

    return (
        np.round(wing_loading_uncorrected, decimals=2),
        np.round(wing_loading_corrected, decimals=2),
        np.round(wing_areas, decimals=2),
        np.round(thrust_to_weight, decimals=2),
        np.round(thrust, decimals=2),
    )
