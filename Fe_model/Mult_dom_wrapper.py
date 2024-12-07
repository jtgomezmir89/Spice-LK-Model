import numpy as np
import lt_spice_model
import pandas as pd
import matplotlib.pyplot as plt

# --- Obtain Target Data --- #######################################################

file_path = 'Data.xlsx'
sheet_name = 'HZO(1-1)'

# Read the sheet and skip rows to identify data
df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)

df.columns = df.columns.str.strip()  # Strip whitespace
df = df.dropna(how='all', axis=1)  # Remove completely empty columns
# centramos los loops

for col in ['Vforce', 'Vforce.1', 'Vforce.2', 'Vforce.3']:
    df[col] = df[col] - (df[col].max() + df[col].min()) / 2

for col in ['Charge', 'Charge.1', 'Charge.2', 'Charge.3']:
    df[col] = df[col] - (df[col].max() + df[col].min()) / 2


df2 = pd.read_excel(file_path, sheet_name='PUND_PW1us', skiprows=3)
df2.columns = df2.columns.str.strip()  # Strip whitespace
df2 = df2.dropna(how='all', axis=1)  # Remove completely empty columns


# --- Ferroelectric parameters --- #################################################
domains = 100
Area = 2500e-8 #cm^2 
Parasitic_resistance = 5e4#4e8
Parasitic_capacitance = 0.19e-9#0.18e-9

mean_Vc = 0.45#0.4
std_dev_Vc = 0.3#0.18

mean_tau = 1e-7 
std_dev_tau = 1e-8

Qo = 0.28e-9
mean_Qo = Qo/domains
std_dev_Qo = mean_Qo * 0.1
Co = 0.33e-9#0.28e-9#0.33e-9
offset = -0.2
Vc_values = np.random.normal(mean_Vc, std_dev_Vc, domains)
#Vc_values = np.random.uniform(-0.3, 1.5, domains )
#for i in range(0,len(Vc_values)):
#    if (Vc_values[i] - offset)<=0:
#        Vc_values[i] = abs(Vc_values[i])
plt.hist(Vc_values, bins=30, alpha=0.7, color='blue', edgecolor='black')
#Vc_values = np.random.uniform(0.1, 1.5, domains )
tau_values = np.random.normal(mean_tau, std_dev_tau, domains)
Qo_values = np.random.normal(mean_Qo, std_dev_Qo, domains)
Qo_values *= Qo/np.sum(Qo_values) # Nos asegurameos que los valores sumen Qo
Qo_values = (Co*abs(Vc_values)**1)/(np.sum(abs(Vc_values)**1)) # la cargar es proporcional al voltaje vcoercivo

lt_spice_model.generate_model(domains, Vc_values, Qo_values, tau_values, offset, Parasitic_resistance, Parasitic_capacitance)

# --- Run Sim and data anlysis --- #################################################

voltages = np.array([0.5,1 , 2])#np.array([0.5, 1, 1.5, 2])
data_sim={}

# PV - loops
for v in voltages:
    print("Voltage:", v)
    data_sim[v]={}
    lt_spice_model.generate_sim(v)
    data = lt_spice_model.run_spice()
    #print(data['variables']) # Revisamos las variables que extraemos
    data_sim = lt_spice_model.analyze_result(data, v, data_sim)

# Simulacion dinamica

data_sim_dyn={}
print("Simualcion dinamica")
lt_spice_model.generate_sim_dyn()
data = lt_spice_model.run_spice()
data_sim_dyn = lt_spice_model.analyze_result_dyn(data, data_sim_dyn)


# --- Ploting --- #################################################

skip = 0 # numero de elementos que voy a saltar 
lt_spice_model.plot_data(data_sim, data_sim_dyn, voltages, df, df2, Area, skip)


