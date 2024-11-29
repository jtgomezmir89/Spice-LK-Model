import numpy as np
import lt_spice_model
#Ferroelectric parameters
domains = 10

mean_Vc = 1 
std_dev_Vc = 0.1

mean_tau = 1e-8 
std_dev_tau = 1e-9

Qo = 1
mean_Qo = Qo/domains
std_dev_Qo = mean_Qo * 0.1

Vc_values = np.random.normal(mean_Vc, std_dev_Vc, domains)
tau_values = np.random.normal(mean_tau, std_dev_tau, domains)
Qo_values = np.random.normal(mean_Qo, std_dev_Qo, domains)

Qo_values *= Qo/np.sum(Qo_values) # Nos asegurameos que los valores sumen Qo

lt_spice_model.generate_model(domains, Vc_values, Qo_values, tau_values)
data = lt_spice_model.run_spice()
#print(data['variables']) # Revisamos las variables que extraemos
data_sim = lt_spice_model.analyze_result(data)

print(data_sim)

#Generate netlist