from takeoff_weight import *
from wing_loading_thrust_weight import *
from liftCoefficient import *
from refined_weight_estimate import *
from initial_wing_sizing import *
from tail_sizing import *
from aero_prop_analysis import *
from static_stability import *
from super_aero_prop_analysis import *
from trim_analysis import *

# from trim_analysis import *

# todo-> questions: do we calculate W/S at stall, and if so, is that the lowest W/S value?
# todo: fsolve to make tails areas work
# todo: supersonic thrust to drag plot (12.4.2, 12.4.5, 12.5.9, and 12.5.10)

# cruise altitude specs (at 45,000 ft)
temp_cruise = 390  # in deg R
density_cruise = 4.62 * 10 ** (-4)  # in slug/ft^3
dynamic_visc = 2.969 * 10 ** (-7)  # in slug/ft-s

# loiter characteristics (at 40,000 ft)
density_loiter = 5.87 * 10 ** (-4)

# original plane specs
R_sub = 1000  # in mi
R_super = 10  # in mi
SFC = 0.9  # in 1/hr
SFC_super = 1.5  # in 1/hr
V_c = 600  # in mph
M_super = 1.25
combat = 1.25  # in hr
loiter = 0.5  # in hr
num_crew = 2
payload = 0  # in lbf

e_0 = 0.8
b_w = 24  # in ft
S_wing = 166  # in ft^2

engine_weight = 3000  # in lbf

# wing parameters
c_l_max = 1.7  # from the airfoil plots
xc_max = 0.83  # location of the maximum (x/c)
tc = 0.14  # maximum thickness
lift_slope = 6.5  # lift/radians
cm_wing = 0.087  # moment coefficient of the airfoil

# calculated values
gamma = 1.4
gas_constant = 1716  # in ft-lbf/slug-R
V_super = M_super * np.sqrt(gamma * gas_constant * temp_cruise)

# tail parameters
wing_location = 7  # in ft, from the nose
tail_end_v = 1  # in ft, from the end of the plane
tail_end_h = 3  # in ft, from the end of the plane
lift_slope_h = 5.3  # todo: fix this value

# run the takeoff weight sizing
(
    iteration_table,
    empty_weight,
    intermediate_weights,
) = initial_weight_estimate(
    temp_cruise=temp_cruise,
    R_sub=R_sub,
    R_super=R_super,
    SFC=SFC,
    SFC_super=SFC_super,
    V_c=V_c,
    M_super=M_super,
    combat_length=combat,
    loiter_length=loiter,
    num_crew=num_crew,
    w_payload=payload,
)

(
    takeoff_weight,
    W_climb,
    W_cruise,
    W_supersonic,
    W_combat,
    W_loiter,
    W_landing,
    W_final,
) = intermediate_weights
w_cruise = (W_supersonic + W_cruise) / 2
w_loiter = (W_landing + W_loiter) / 2
w_supersonic = (W_supersonic + W_combat) / 2

a = 0.87
c = 0.4
fuselage_length = np.round(a * takeoff_weight**c, decimals=0)

print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")
print("The takeoff weight in lbf is: ", takeoff_weight)
print("The following show fsolve iterations: ", iteration_table)
print("The empty weight in lbf is: ", empty_weight)
print("The fuselage length in ft is: ", fuselage_length)
print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")


# find the lift coefficient
cl, cl_super, Re, M_subsonic = lift_coeff_estimate(
    V_c=V_c,
    W_cruise=w_cruise,
    W_supersonic=w_supersonic,
    bw=b_w,
    S_wing=S_wing,
    cruise_density=density_cruise,
    V_super=V_super,
    dynamic_visc=dynamic_visc,
    temp_cruise=temp_cruise,
)

print("The required coefficient of lift at cruise is: ", cl)
print("The required coefficient of lift at supersonic dash is: ", cl_super)
print("The Reynolds number at cruise is: ", Re)
print("The Mach number at cruise is: ", M_subsonic)
print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")

(
    [S_wing, b_w, AR_wing, avg_chord, sweep_angle, c_tip, c_root, quarter_chord, Y_wing]
) = initial_wing_sizing(takeoff_weight, M_subsonic)

print("Adjusted for historic trends:")
print("The area of the wing in ft^2 is: ", S_wing)
print("The span in ft of the wing is: ", b_w)
print("The average chord in ft is: ", avg_chord)
print("The aspect ratio is: ", AR_wing)
print("The sweep angle in deg is: ", sweep_angle)
print("The tip and root chords in ft are: ", c_tip, " and ", c_root, "respectively")
print("The quarter-chord length in ft is: ", quarter_chord)
print("The length from the center line to the average chord is: ", Y_wing)
print("~~~~~~~~~~~~~~~~~~~~~~~")

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
] = tail_sizing(
    S_wing=S_wing,
    fuselage_length=fuselage_length,
    wing_location=wing_location,
    tail_end_v=tail_end_v,
    tail_end_h=tail_end_h,
    Y_w=Y_wing,
    sweep_angle_wing=sweep_angle,
    quarter_chord_w=quarter_chord,
    avg_chord_w=avg_chord,
    b_wing=b_w,
)
print("Vertical tail characteristics:")
print(
    "Chord lengths: tip - ",
    c_tip_v,
    ", root - ",
    c_root_v,
    ", average - ",
    avg_chord_v,
    ", quarter - ",
    quarter_chord_v,
)
print("Taper ratio: ", taper_ratio_v)
print("Span - ", b_v, ", wing area - ", S_v, ", and aspect ratio - ", AR_v)
print("Moment arm - ", Y_v)

print("~~~~~~~~~~~~~~~~~~~~~~~")

print("Horizontal tail characteristics:")
print(
    "Chord lengths: tip - ",
    c_tip_h,
    ", root - ",
    c_root_h,
    ", average - ",
    avg_chord_h,
    ", quarter - ",
    quarter_chord_h,
)
print("Taper ratio: ", taper_ratio_h)
print("Span - ", b_h, ", wing area - ", S_h, ", and aspect ratio - ", AR_h)
print("Moment arm - ", Y_h)

print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")

# added a for loop to make these values converge a little nicer:
err = 1
takeoff_weight_initial = takeoff_weight
while err > 0.1:
    (
        wing_loading_uncorrected,
        wing_loading_corrected,
        wing_areas,
        thrust_to_weight,
        thrust,
    ) = wing_loading(
        W0=takeoff_weight,
        cruise_density=density_cruise,
        loiter_density=density_loiter,
        temp_cruise=temp_cruise,
        V_c=V_c,
        M_super=M_super,
        M_sub=M_subsonic,
        e_0=0.8,
        b_w=b_w,
        S_w=S_wing,
        takeoff_weight=takeoff_weight,
        w_cruise=w_cruise,
        w_loiter=w_loiter,
        w_supersonic=w_supersonic,
        w_landing=W_landing,
        c_l_max=c_l_max,
    )

    # todo: know this is static
    refined_wing_area = wing_areas[1]

    AR_wing = b_w**2 / refined_wing_area
    takeoff_weight_old = takeoff_weight
    wing_loading_refined_weight = (
        wing_loading_corrected[0],
        wing_loading_corrected[1],
        wing_loading_corrected[2],
        wing_loading_corrected[4],
    )
    (
        iteration_table,
        empty_weight,
        intermediate_weights,
        fuel_fraction_cruise,
    ) = refined_weight_estimate(
        temp_cruise=temp_cruise,
        R_sub=R_sub,
        R_super=R_super,
        SFC=SFC,
        SFC_super=SFC_super,
        V_c=V_c,
        M_super=M_super,
        combat_length=combat,
        loiter_length=loiter,
        num_crew=num_crew,
        w_payload=payload,
        L2D_sub=thrust_to_weight[1] ** (-1),
        L2D_loiter=thrust_to_weight[3] ** (-1),
        L2D_super=thrust_to_weight[2] ** (-1),
        L2D_combat=thrust_to_weight[3] ** (-1),
        T2W=thrust_to_weight[0],  # thrust to weight at takeoff
        W2S=min(wing_loading_refined_weight),  # minimum value, disregarding loiter
        AR=AR_wing,
        M_subsonic=M_subsonic,
    )

    err = (takeoff_weight - takeoff_weight_old) / takeoff_weight_old


print("Wing loading uncorrected at takeoff: ", wing_loading_uncorrected[0])
print("Wing loading uncorrected at cruise: ", wing_loading_uncorrected[1])
print("Wing loading uncorrected at supersonic dash: ", wing_loading_uncorrected[2])
print("Wing loading uncorrected at loiter: ", wing_loading_uncorrected[3])
print("Wing loading uncorrected at landing: ", wing_loading_uncorrected[4])

print("~~~~~~~~~~~~~~~~~~~~~~~")

print("Wing loading corrected at takeoff: ", wing_loading_corrected[0])
print("Wing loading corrected at cruise: ", wing_loading_corrected[1])
print("Wing loading corrected at supersonic dash: ", wing_loading_corrected[2])
print("Wing loading corrected at loiter: ", wing_loading_corrected[3])
print("Wing loading corrected at landing: ", wing_loading_corrected[4])

print("~~~~~~~~~~~~~~~~~~~~~~~")

print("List of new wing areas in ft^2: ", wing_areas)
print("Refined wing area in ft^2: ", refined_wing_area)
print(
    "Percent change in wing area: ",
    np.round((refined_wing_area - S_wing) / S_wing * 100, decimals=2),
)
S_wing = refined_wing_area

print("~~~~~~~~~~~~~~~~~~~~~~~")

print("Thrust to weight ratio at takeoff: ", thrust_to_weight[0])
print("Thrust to weight ratio at cruise: ", thrust_to_weight[1])
print("Thrust to weight ratio at supersonic dash: ", thrust_to_weight[2])
print("Thrust to weight ratio at loiter: ", thrust_to_weight[3])
print("Thrust to weight ratio at landing: ", thrust_to_weight[4])

print("~~~~~~~~~~~~~~~~~~~~~~~")

print("Thrust in lbf at takeoff: ", thrust[0])
print("Thrust in lbf at cruise: ", thrust[1])
print("Thrust in lbf at supersonic dash: ", thrust[2])
print("Thrust in lbf at loiter: ", thrust[3])
print("Thrust in lbf at landing: ", thrust[4])

print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")

(
    takeoff_weight,
    W_climb,
    W_cruise,
    W_supersonic,
    W_combat,
    W_loiter,
    W_landing,
    W_final,
) = intermediate_weights

print("The takeoff weight in lbf is: ", takeoff_weight)
print("The following show fsolve iterations: ", iteration_table)
print("The empty weight in lbf is: ", empty_weight)
print(
    "The percent change in takeoff weight is: ",
    np.round(
        (takeoff_weight - takeoff_weight_initial) / takeoff_weight_initial * 100,
        decimals=2,
    ),
)

print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")

w_cruise = (W_supersonic + W_cruise) / 2
w_loiter = (W_landing + W_loiter) / 2
w_supersonic = (W_supersonic + W_combat) / 2


cl, cl_super, Re, M_subsonic = lift_coeff_estimate(
    V_c=V_c,
    W_cruise=w_cruise,
    W_supersonic=w_supersonic,
    bw=b_w,
    S_wing=S_wing,
    cruise_density=density_cruise,
    V_super=V_super,
    dynamic_visc=dynamic_visc,
    temp_cruise=temp_cruise,
)

print("After the refined weight estimate:")
print("The required coefficient of lift at cruise is: ", cl)
print("The required coefficient of lift at supersonic dash is: ", cl_super)
print("The Reynolds number at cruise is: ", Re)
print("The Mach number at cruise is: ", M_subsonic)
print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")

v_star = propulsion_analysis(
    c_l_max=c_l_max,
    w_landing=W_landing,
    cruise_density=density_cruise,
    S_wing=refined_wing_area,
    V_c=V_c,
    AR_wing=AR_wing,
    w_cruise=w_cruise,
    takeoff_weight=takeoff_weight,
    cruise_temp=temp_cruise,
    Re_wing=Re,
    xc_max=xc_max,
    tc=tc,
    sweep_angle=sweep_angle,
    c_h_tail=avg_chord_h,
    c_v_tail=avg_chord_v,
    S_h_tail=S_h,
    S_v_tail=S_v,
    fuselage_length=fuselage_length,
    M_subsonic=M_subsonic,
    dynamic_visc=dynamic_visc,
    cruise_thrust=thrust[1],
    M_super=M_super,
)

print("Subsonic V* in ft/s is: ", v_star)
print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")

v_star_super = super_propulsion_analysis(
    c_l_max=c_l_max,
    w_landing=W_landing,
    cruise_density=density_cruise,
    S_wing=refined_wing_area,
    V_c=V_c,
    AR_wing=AR_wing,
    w_cruise=w_cruise,
    takeoff_weight=takeoff_weight,
    cruise_temp=temp_cruise,
    Re_wing=Re,
    xc_max=xc_max,
    tc=tc,
    sweep_angle=sweep_angle,
    c_h_tail=avg_chord_h,
    c_v_tail=avg_chord_v,
    S_h_tail=S_h,
    S_v_tail=S_v,
    fuselage_length=fuselage_length,
    M_subsonic=M_subsonic,
    dynamic_visc=dynamic_visc,
    cruise_thrust=thrust[1],
    thrust_supersonic=thrust[2],
    M_super=M_super,
    avg_chord=avg_chord,
)

print("Supersonic V* in ft/s is: ", v_star_super)
print("~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~")

fineness_ratio = 12  # based on pg 157
fuselage_diameter = fuselage_length / fineness_ratio  # fuselage diameter - FIX
h_nose = fuselage_diameter
S_wet_noseandback = (
    2
    * math.pi
    * (fuselage_diameter / 2)
    * math.sqrt((fuselage_diameter / 2) ** 2 + h_nose**2)
)
S_fuselage = (math.pi * fuselage_length * fuselage_diameter) + S_wet_noseandback


W_fuel = fuel_fraction_cruise * takeoff_weight  # todo: this needs to be changed

x_cg = center_of_gravity(
    S_v_tail=S_v,
    S_h_tail=S_h,
    S_wing=S_wing,
    S_fuselage=S_fuselage,
    takeoff_weight=takeoff_weight,
    engine_weight=engine_weight,
    avg_chord=avg_chord,
    wing_location=wing_location,
    fuselage_length=fuselage_length,
    h_tail_end=tail_end_h,
    c_root_h=c_root_h,
    c_h_tail=avg_chord_h,
    v_tail_end=tail_end_v,
    c_root_v=c_root_v,
    c_v_tail=avg_chord_v,
    w_fuel=W_fuel,
    fuel_location=wing_location,
    landing_location=0.75,
    engine_location=0.7,
    Y_wing=Y_wing,
    sweep_angle=sweep_angle,
    Y_v_tail=Y_v,
    Y_h_tail=Y_h,
)
print("The location of the center of gravity from the nose is: ", x_cg)
wing_25 = np.round(
    wing_location + Y_wing * np.tan(sweep_angle) + quarter_chord, decimals=2
)
wing_35 = np.round(
    wing_location + Y_wing * np.tan(sweep_angle) + 0.35 * avg_chord, decimals=2
)
print("25% of the wing to 35% of the wing is: ", wing_25, " - ", wing_35)


fuselage_weight = 4.8 * S_fuselage
x_np = neutral_point(
    quarter_chord=quarter_chord,
    avg_chord=avg_chord,
    S_wing=S_wing,
    M_subsonic=M_subsonic,
    quarter_c_h=quarter_chord_h,
    S_h_tail=S_h,
    Cl_alpha=lift_slope,
    AR_wing=AR_wing,
    sweep_angle=sweep_angle,
    fuselage_diameter=fuselage_diameter,
    fuselage_length=fuselage_length,
    fuselage_weight=fuselage_weight,
    c_root=c_root,
    b_w=b_w,
    c_root_h=c_root_h,
    AR_h_tail=AR_h,
    Cl_alpha_h=lift_slope_h,
    wing_location=wing_location,
    Y_wing=Y_wing,
    h_tail_end=tail_end_h,
    Y_h_tail=Y_h,
)

print("The location of the neutral point is: ", x_np)

static_margin = x_np - x_cg
print("The static margin is: ", static_margin)

trim_analysis(
    M_subsonic=M_subsonic,
    Cl_alpha=lift_slope,
    S_wing=S_wing,
    fuselage_diameter=fuselage_diameter,
    c_root=c_root,
    b_w=b_w,
    AR_wing=AR_wing,
    sweep_angle=sweep_angle,
    c_root_h=c_root_h,
    S_h_tail=S_h,
    AR_h_tail=AR_h,
    Cl_alpha_h=lift_slope_h,
    wing_location=wing_location,
    Y_wing=Y_wing,
    avg_chord=avg_chord,
    quarter_chord=quarter_chord,
    quarter_c_h=quarter_chord_h,
    fuselage_length=fuselage_length,
    h_tail_end=tail_end_h,
    Y_h_tail=Y_h,
    c_h_tail=avg_chord_h,
    Cm_airfoil=cm_wing,
)
