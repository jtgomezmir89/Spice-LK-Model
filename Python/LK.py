from pylab import *
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec
import numpy as np
from sympy import *
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import math


rho = 0.01
Vc = 0.5
Qo = 0.1
Co = Qo/Vc
tau = rho*Co
k = 3*np.sqrt(3)/2#3*np.sqrt(3)/2

print("k: ", k)
print("tau: ", tau)

def df(t, Qn, Vn):
    dQn_dt = (Vn + k * Qn - k * Qn**3)/tau
    return dQn_dt

def df_II(t, Qn, Vn):
    dQn_dt = (Vn + k * Qn - k * Qn**3)/(tau + tau*Qn**2)
    return dQn_dt

def df_III(t, Qn, Vn):
    #dQn_dt = (Vn + k*(Qn - Qn**3 - (3/5)*Qn**5 - (3/7)*Qn**7))/(tau*(1 + Qn**2 + Qn**4 + Qn**6))
    dQn_dt = (Vn + k*(Qn - Qn**3 - (3/5)*Qn**5 - (3/7)*Qn**7))/(tau*(1 + Qn**2 + Qn**4 + Qn**6))
    return dQn_dt

def df_IV(t, Qn, Vn):
    Qn = np.clip(Qn, -0.99999999999, 0.99999999999)
    arctanh_Qn = np.arctanh(Qn) 
    dQn_dt = ((1 - Qn**2) / tau) * (Vn - 3 * k * arctanh_Qn + 4 * k * Qn)
    return dQn_dt

def df_V(t, Qn, Vn):
    Qn = np.clip(Qn, -0.99999999999, 0.99999999999)
    arctanh_Qn = np.arctanh(Qn) 
    k1= 2.62    #4.03,2.49,3.91,2.6
    k2=1 #0.77*k1-1.02#2.1,0.9,2,1
    print("k1:", k1)
    print("k2:", k2)
    dQn_dt = ((1 - Qn**2) / tau) * (Vn +k1* Qn - k2*arctanh_Qn) #sale de la implementación en spice
    #dQn_dt = ((1 - Qn**2) / tau) * (k1*Vn +k3*k1*Qn -arctanh_Qn)
    return dQn_dt


Vfe_up = np.linspace(-2, 2, 500)
Vfe_down = np.linspace(2, -2, 500)
Vfe_values = np.concatenate((Vfe_up, Vfe_down))
Vn_values = Vfe_values


Qn_final_values = []
Qn_final_values_II = []
Qn_final_values_III = []
Qn_final_values_IV = []
Qn_final_values_V = []

t_span = (0, 3)
Qn_initial = [-1]
Qn_initial_II = [-1]
Qn_initial_III = [-1]
Qn_initial_IV= [-1]
Qn_initial_V= [-1]


# Solve the differential equation for each value of Vfe
for Vn in Vn_values:
    #solution = solve_ivp(df, t_span, Qn_initial, args=(Vn,), t_eval=[t_span[1]])
    #Qn_final_values.append(solution.y[0][-1])
    #Qn_initial = [solution.y[0][-1]]

    #solution_II = solve_ivp(df_II, t_span, Qn_initial_II, args=(Vn,), t_eval=[t_span[1]])
    #Qn_final_values_II.append(solution_II.y[0][-1])
    #Qn_initial_II = [solution_II.y[0][-1]]

    #solution_III = solve_ivp(df_III, t_span, Qn_initial_III, args=(Vn,), t_eval=[t_span[1]])
    #Qn_final_values_III.append(solution_III.y[0][-1])
    #Qn_initial_III = [solution_III.y[0][-1]]

    #solution_IV = solve_ivp(df_IV, t_span, Qn_initial_IV, args=(Vn,), t_eval=[t_span[1]]) 
                            #max_step=0.001, 
                            #rtol=1e-7, 
                            #atol=1e-9,
                            #method='DOP853')       
    #Qn_final_values_IV.append(solution_IV.y[0][-1])
    #Qn_initial_IV = [solution_IV.y[0][-1]]

    solution_V = solve_ivp(df_V, t_span, Qn_initial_V, args=(Vn,), t_eval=[t_span[1]],
                            max_step=0.01, 
                            rtol=1e-6, 
                            atol=1e-8,
                            method='DOP853')          
    Qn_final_values_V.append(solution_V.y[0][-1])
    Qn_initial_V = [solution_V.y[0][-1]]
    #print(Vn)



plt.figure(figsize=(8, 6))  # Increase figure size

plt.axvline(x=1, color='k', linestyle=':', linewidth=1)
plt.axvline(x=-1, color='k', linestyle=':', linewidth=1)
plt.axhline(y=1, color='k', linestyle=':', linewidth=1)
plt.axhline(y=-1, color='k', linestyle=':', linewidth=1)


#plt.plot(Vfe_values, Qn_final_values, label=r'df', color='cyan', linewidth=6)
#plt.plot(Vfe_values, Qn_final_values_II, label=r'df_II', color='coral', linestyle='-', linewidth=3)
#plt.plot(Vfe_values, Qn_final_values_III, label=r'df_III', color='springgreen', linestyle='--', linewidth=2.5)
#plt.plot(Vfe_values, Qn_final_values_IV, label=r'df_IV', color='k', linestyle='--', linewidth=1.5)
plt.plot(Vfe_values, Qn_final_values_V, label=r'df_V', color='green', linestyle='--', linewidth=2)

plt.xlabel('$V_N$', fontsize=20)
plt.ylabel('$Q_N$', fontsize=20)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=14, width=2, length=7)
plt.tick_params(axis='both', which='minor', labelsize=12, width=1, length=4)

plt.legend(fontsize=14, loc='upper left')

plt.show()