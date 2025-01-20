import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec

# Reading the data from the file
file_path = "./coupled_oscillators.txt"
data = pd.read_csv(file_path, delim_whitespace=True)

# Extracting columns for plotting
time = data['time'] * 1000  # Convert time to milliseconds
v_s = data['V(s)']
v_s1 = data['V(s1)']
v_s2 = data['V(s2)']
v_s3 = data['V(s3)']

# Limits for the first plot
Lower_mark1 = 0
Upper_mark1 = 30  # Convert to ms
time_range_mask1 = (time >= Lower_mark1) & (time <= Upper_mark1)
time_filtered1 = time[time_range_mask1]
v_s_filtered1 = v_s[time_range_mask1]
v_s1_filtered1 = v_s1[time_range_mask1]
v_s2_filtered1 = v_s2[time_range_mask1]
v_s3_filtered1 = v_s3[time_range_mask1]

# Limits for the second plot
Lower_mark2 = 25  # Convert to ms
Upper_mark2 = 30  # Convert to ms
time_range_mask2 = (time >= Lower_mark2) & (time <= Upper_mark2)
time_filtered2 = time[time_range_mask2]
v_s_filtered2 = v_s[time_range_mask2]
v_s1_filtered2 = v_s1[time_range_mask2]
v_s2_filtered2 = v_s2[time_range_mask2]
v_s3_filtered2 = v_s3[time_range_mask2]

# Calculating differences for the second plot
vs_minus_vs2 = v_s1_filtered2 - v_s2_filtered2
vs1_minus_vs3 = v_s_filtered2 - v_s3_filtered2

# Create figure and gridspec layout
fig = plt.figure()
gs = GridSpec(3, 10, height_ratios=[1, 1, 1])

# First subplot: Oscillators vs time (Filtered Range)
ax1 = fig.add_subplot(gs[0, :9])  # Use the first two columns of the top row
ax1.plot(time_filtered1, v_s_filtered1, label="V(s1)", color="#0028ff")     # Blue
ax1.plot(time_filtered1, v_s1_filtered1, label="V(s2)", color="#f47f15")   # Orange
ax1.plot(time_filtered1, v_s2_filtered1, label="V(s3)", color="#68fb0d")   # Green
ax1.plot(time_filtered1, v_s3_filtered1, label="V(s4)", color="#f30606")   # Red

# Set axis labels
ax1.set_xlabel("Time (ms)", fontsize=18)  # Moved label outside
ax1.set_ylabel("Voltage (V)", fontsize=18)

# Set y-axis limits for better visualization of oscillations
ax1.set_ylim(0.4, 0.85)

# Adjust tick label size
ax1.tick_params(axis='both', which='major', labelsize=14)

# Highlight the range used for the second plot
ax1.axvspan(
    Lower_mark2, Upper_mark2, color="red", alpha=0.3,
)
ax1.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1.02, 0.85))
ax1.grid(True)

# Second subplot: V(s3) - V(s2) vs V(s) - V(s1)
ax2 = fig.add_subplot(gs[1:, :])  # Use the entire bottom row
ax2.plot(vs_minus_vs2, vs1_minus_vs3, color=plt.cm.winter(0.5))

# Set axis labels
ax2.set_xlabel("V(s2) - V(s3) (V)", fontsize=18)
ax2.set_ylabel("V(s1) - V(s4) (V)", fontsize=18)

# Adjust tick label size
ax2.tick_params(axis='both', which='major', labelsize=14)

# ax2.grid(True)

# Adjust layout to separate the plots vertically
plt.subplots_adjust(hspace=0.5)  # Increased vertical and horizontal spacing

# Display the plot
plt.tight_layout()
plt.show()
