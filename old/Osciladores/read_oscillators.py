import matplotlib.pyplot as plt
import pandas as pd

# Reading the data from the file
file_path = "Neuron_oscillator_coupled_oscillators.txt"
data = pd.read_csv(file_path, delim_whitespace=True)

# Extracting columns for plotting
time = data['time']
v_s = data['V(out_1)']
v_s1 = data['V(out_2)']
v_s2 = data['V(out_3)']
v_s3 = data['V(out_4)']

# Filtering data for the second plot
Lower_mask = 0.25
Upper_mask = 1
time_range_mask = (time >= Lower_mask) & (time <= Upper_mask )
time_filtered = time[time_range_mask]
v_s_filtered = v_s[time_range_mask]
v_s1_filtered = v_s1[time_range_mask]
v_s2_filtered = v_s2[time_range_mask]
v_s3_filtered = v_s3[time_range_mask]

# Calculating differences for the second plot
vs_minus_vs2 = v_s_filtered - v_s3_filtered
vs1_minus_vs3 = v_s1_filtered - v_s2_filtered

# Creating the combined figure
fig, axs = plt.subplots(2, 1, figsize=(10, 12), gridspec_kw={'height_ratios': [1, 2]})

# First subplot: Oscillators vs time
axs[0].plot(time, v_s, label="V(out_1)", color=plt.cm.winter(0.2))
axs[0].plot(time, v_s1, label="V(out_2)", color=plt.cm.winter(0.4))
axs[0].plot(time, v_s2, label="V(out_3)", color=plt.cm.winter(0.6))
axs[0].plot(time, v_s3, label="V(out_4)", color=plt.cm.winter(0.8))
axs[0].set_xlabel("Time (out_1)")
axs[0].set_ylabel("Voltage (V)")
axs[0].legend()
axs[0].grid(True)

# Marking the time range with a square
axs[0].axvspan(Lower_mask, Upper_mask, color='red', alpha=0.3, 
               label=f"Time Range ({Lower_mask}-{Upper_mask} s)")
axs[0].legend()

# Second subplot: V(out_1) - V(out_3) vs V(out_2) - V(out_4)
axs[1].plot(vs_minus_vs2, vs1_minus_vs3, color=plt.cm.winter(0.5))
axs[1].set_xlabel("V(out_1) - V(out_4) (V)")
axs[1].set_ylabel("V(out_2) - V(out_3) (V)")
axs[1].grid(True)

# Adjust layout and display the plot
plt.tight_layout()
plt.show()