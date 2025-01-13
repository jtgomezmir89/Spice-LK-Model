import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
import matplotlib.colors as mcolors

# Initialize a dictionary to hold data for each step
data = {}
current_step = None

# Open and read the file
file_path = 'Fe_test_tau2.txt'

with open(file_path, 'r', encoding='ISO-8859-1') as f:
    for line in f:
        step_match = re.match(r'Step Information: (.*)', line)
        if step_match:
            current_step = step_match.group(1)
            data[current_step] = {'time': [], 'V(in)': [], 'V(q)': []}
        
        # Check if the line contains data values
        elif current_step and re.match(r'\d', line):
            # Split the line into columns and append values to the current step's data
            cols = line.split()
            data[current_step]['time'].append(float(cols[0]))
            data[current_step]['V(in)'].append(float(cols[1]))
            data[current_step]['V(q)'].append(float(cols[2]))

# List to hold step values converted to seconds and original labels
step_values_seconds = []
step_labels = []

# Convert step values with units to seconds
for step in data.keys():
    vec = re.split(r'[= ]', step)
    step_str = vec[1]  # Extract the value with unit, e.g., "1n" or "2µ"
    print(step_str)
    # Convert based on unit
    if 'n' in step_str:
        numeric_value = float(step_str.replace('n', '')) * 1e-9  # Convert nanoseconds to seconds
    elif 'µ' in step_str or 'u' in step_str:  # Check for both "µ" and "u" for microseconds
        numeric_value = float(step_str.replace('µ', '').replace('u', '')) * 1e-6  # Convert microseconds to seconds
    else:
        numeric_value = float(step_str)  # If no unit, assume it's already in seconds

    step_values_seconds.append(numeric_value)  # Store the converted value in seconds
    step_labels.append(step_str)  # Keep original string for labels

# Set up the viridis colormap and logarithmic normalization with vmin and vmax
vmin = min(step_values_seconds)
vmax = max(step_values_seconds)
norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
viridis = plt.cm.get_cmap('winter', len(data))

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

plt.axvline(x=1, color='k', linestyle=':', linewidth=1)
plt.axvline(x=-1, color='k', linestyle=':', linewidth=1)
plt.axhline(y=1, color='k', linestyle=':', linewidth=1)
plt.axhline(y=-1, color='k', linestyle=':', linewidth=1)

# Plot each step with a unique color based on the logarithmic color normalization

ini = 170  # Assuming `ini` is the start index for slicing `values`

for i, (step, values) in enumerate(reversed(list(data.items()))):
    color = viridis(norm(step_values_seconds[-(i + 1)]))  # Get color based on normalized log scale
    ax.plot(
        values['V(in)'][ini:], 
        values['V(q)'][ini:], 
        linewidth=2,
        color=color  # Use color from viridis colormap
    )




# Create a color bar on the right with logarithmic scale
sm = plt.cm.ScalarMappable(cmap=viridis, norm=norm)
sm.set_array([])  # Dummy array for ScalarMappable
cbar = fig.colorbar(sm, ax=ax)  # Removed extend='both'
cbar.set_label(r'$\tau_p$ (seconds)', labelpad=25, rotation=270, fontsize=15)
cbar.ax.tick_params(labelsize=12) 
# Define major ticks at key points only to keep it simple and readable
major_ticks = [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 5e-5]
cbar.set_ticks(major_ticks)

# Format color bar tick labels with original units
def format_tick_label(value):
    """Convert seconds back to appropriate unit with 'n' or 'µ'."""
    if value >= 1e-6:  # Convert to microseconds
        return f"{value / 1e-6:.0f}µ"
    elif value >= 1e-9:  # Convert to nanoseconds
        return f"{value / 1e-9:.0f}n"
    else:  # Default to seconds if no match
        return f"{value:.0g}s"

cbar.set_ticklabels([format_tick_label(tick) for tick in major_ticks])


plt.xlabel('$V_N$', fontsize=20)
plt.ylabel('$Q_N$', fontsize=20)

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.minorticks_on()
plt.tick_params(axis='both', which='major', labelsize=14, width=2, length=7)
plt.tick_params(axis='both', which='minor', labelsize=12, width=1, length=4)


plt.show()