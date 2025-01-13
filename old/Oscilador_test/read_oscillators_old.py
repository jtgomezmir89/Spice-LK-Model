import matplotlib.pyplot as plt
import pandas as pd

# Reading the data from the file
file_path = "./Oscilador_coupled_transistors.txt"
data = pd.read_csv(file_path, delim_whitespace=True)

# Extracting columns for plotting
time = data['time']
v_s = data['V(s)']
v_s1 = data['V(s1)']
v_s2 = data['V(s2)']
v_s3 = data['V(s3)']

# Filtering data for the second plot
Lower_mask = 0.14
Upper_mask = 0.15
time_range_mask = (time >= Lower_mask) & (time <= Upper_mask)
time_filtered = time[time_range_mask]
v_s_filtered = v_s[time_range_mask]
v_s1_filtered = v_s1[time_range_mask]
v_s2_filtered = v_s2[time_range_mask]
v_s3_filtered = v_s3[time_range_mask]

# Calculating differences for the second plot
vs_minus_vs2 = v_s3_filtered - v_s2_filtered
vs1_minus_vs3 = v_s_filtered - v_s1_filtered

# Creating the combined figure
fig, axs = plt.subplots(2, 1, figsize=(10, 12), gridspec_kw={'height_ratios': [1, 2]})

# First subplot: Oscillators vs time (Filtered Range)
axs[0].plot(time_filtered, v_s_filtered, label="V(s)", color="#0028ff")     # Blue
axs[0].plot(time_filtered, v_s1_filtered, label="V(s1)", color="#f47f15")   # Orange
axs[0].plot(time_filtered, v_s2_filtered, label="V(s2)", color="#68fb0d")   # Green
axs[0].plot(time_filtered, v_s3_filtered, label="V(s3)", color="#f30606")   # Red

# Increase axis label fonts
axs[0].set_xlabel("Time (s)", fontsize=25)
axs[0].set_ylabel("Voltage (V)", fontsize=25)

# Adjust tick label size
axs[0].tick_params(axis='both', which='major', labelsize=25)

axs[0].legend(fontsize=26)
axs[0].grid(True)
#axs[0].set_ylim(0.5, 0.9)

# Marking the time range with a square
axs[0].axvspan(Lower_mask, Upper_mask, color='red', alpha=0.3,
               label=f"Time Range ({Lower_mask}-{Upper_mask} s)")

# Second subplot: V(s3) - V(s2) vs V(s) - V(s1)
axs[1].plot(vs_minus_vs2, vs1_minus_vs3, color=plt.cm.winter(0.5))

# Increase axis label fonts
axs[1].set_xlabel("V(s3) - V(s2) (V)", fontsize=25)
axs[1].set_ylabel("V(s) - V(s1) (V)", fontsize=25)

# Adjust tick label size
axs[1].tick_params(axis='both', which='major', labelsize=25)

axs[1].grid(True)

# Adjust layout and display the plot
plt.tight_layout()
plt.show()