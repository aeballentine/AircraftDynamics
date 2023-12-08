from takeoff_weight import *
from wing_loading_thrust_weight import *
from liftCoefficient import *
from refined_weight_estimate import *

# cruise altitude specs (at 45,000 ft)
temp_cruise = 390  # in deg R
density_cruise = 4.62 * 10 ** (-4)  # in slug/ft^3
dynamic_visc = 2.969 * 10 ** (-7)  # in slug/ft-s

# loiter characteristics (at 40,000 ft)
density_loiter = 5.87 * 10 ** (-4)

# original plane specs
R_sub = 1200  # in mi
R_super = 75  # in mi
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
S_wing = 164  # in ft^2
c_l_max = 1.7  # from the airfoil plots

# calculated values
gamma = 1.4
gas_constant = 1716  # in ft-lbf/slug-R
V_super = M_super * np.sqrt(gamma * gas_constant * temp_cruise)

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

print("The takeoff weight in lbf is: ", takeoff_weight)
print("The following show fsolve iterations: ", iteration_table)
print("The empty weight in lbf is: ", empty_weight)
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

# takeoff, cruise, supersonic, loiter, landing
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


new_range = 1000  # in mi
new_dash = 10  # in mi
new_AR = 24**2 / refined_wing_area
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
) = refined_weight_estimate(
    temp_cruise=temp_cruise,
    R_sub=new_range,
    R_super=new_dash,
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
    T2W=max(thrust_to_weight),  # max thrust to weight
    W2S=min(wing_loading_refined_weight),  # minimum value
    AR=new_AR,
    M_subsonic=M_subsonic,
)

print(max(thrust_to_weight), min(wing_loading_refined_weight), new_AR, M_subsonic)
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

print("~~~~~~~~~~~~~~~~~~~~~~~")