import numpy as np
import lt_spice_model
import pandas as pd


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



# --- Ferroelectric parameters --- #################################################
domains = 10
Area = 2500e-8 #cm^2 
Parasitic_resistance = 1e9
Parasitic_capacitance = 1e-9

mean_Vc = 1 
std_dev_Vc = 0.1

mean_tau = 1e-8 
std_dev_tau = 1e-9

Qo = 1e-6
mean_Qo = Qo/domains
std_dev_Qo = mean_Qo * 0.1

Vc_values = np.random.normal(mean_Vc, std_dev_Vc, domains)
tau_values = np.random.normal(mean_tau, std_dev_tau, domains)
Qo_values = np.random.normal(mean_Qo, std_dev_Qo, domains)
Qo_values *= Qo/np.sum(Qo_values) # Nos asegurameos que los valores sumen Qo
lt_spice_model.generate_model(domains, Vc_values, Qo_values, tau_values, Parasitic_resistance, Parasitic_capacitance)

# --- Run Sim and data anlysis --- #################################################

voltages = np.array([0.5, 1, 1.5, 2])
data_sim={}

for v in voltages:
    lt_spice_model.generate_sim(v)
    data = lt_spice_model.run_spice()
    #print(data['variables']) # Revisamos las variables que extraemos
    data_sim = lt_spice_model.analyze_result(data, data_sim)



lt_spice_model.plot_data(data_sim, df, Area)


