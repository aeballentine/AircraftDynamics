import math
import matplotlib.pyplot as plt
import numpy as np


def man_analysis(
    V_c,
    W_climb,
    w_landing,
    cruise_density,
    S_wing,
    c_l_max,
    thrust_weight_TO,
):
    # Climb T/W
    V_stall = round(math.sqrt(2 * w_landing / (cruise_density * S_wing * c_l_max)))
    lift_drag_TO = (thrust_weight_TO) ** (-1)
    V_TO = 1.2 * V_stall
    # V_v = V_TO * math.sin(climb_angle)
    V_v = 50  # from lecture 26 in ft/s
    thrust_weight_climb = (V_v / V_TO) + (1 / lift_drag_TO)
    print("Trust-to-weight ratio at climb: ", thrust_weight_climb)
    thrust_climb = thrust_weight_climb * W_climb
    print("Thrust at climb: ", thrust_climb)

    # Turn rate and turn radius
    velocity = []
    TRate = []
    TRadius = []
    for V in range(V_stall, round(1.2 * V_c) + 1):
        # Level turn analysis: turn rate, turn radius
        g = 32.2
        load_factor = 8 * g  # from structural analysis
        turn_rate = (g * math.sqrt((load_factor**2) - 1)) / V
        turn_radius = (V**2) / (g * math.sqrt(load_factor**2 - 1))
        velocity.append(V)
        TRate.append(turn_rate)
        TRadius.append(turn_radius)

    # Plot
    plt.plot(velocity, TRate, color="blue", label="Turn Rate [deg/s]")
    plt.plot(velocity, TRadius, color="red", label="Turn Radius [ft]")
    plt.title("Plot of Turn Rate and Turn Radius vs. Flight Speed")
    plt.legend()
    plt.show()

    return np.round(np.array([thrust_weight_climb, thrust_climb]), decimals=2)
