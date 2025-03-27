# An Optimized SPICE-Compatible Positive Feedback Model for Ferroelectric Devices

This repository contains the simulation files for reproducing and extending the results presented in the paper:

**"An Optimized SPICE-Compatible Positive Feedback Model for Ferroelectric Devices: Design, Calibration, and Dynamic Simulations"**
Authors: Nicolás Villegas, Joaquín Carvajal, Shumiya Alam, Tanvir Pantha, Jaime Cisternas, Kai Ni, Sourav Dutta, Jorge Gómez

## Repository Structure

The repository is organized into the following directories:

1. **`Fe_model/`**Contains the SPICE-compatible single-domain ferroelectric model. This folder includes:

   - SPICE netlists for the Landau-Khalatnikov (L-K) equivalent model.
   - Calibration scripts for static and dynamic behavior.
   - Calibration and validation against experimental data.
   - Example simulations for polarization-voltage (P-V) and polarization switching dynamics.
2. **`Fe_leakage_model/`**Includes an extended version of the ferroelectric model with leakage current and parasitic capacitance. This folder provides:

   - Circuit files accounting for non-idealities in ferroelectric capacitors.
   - Simulations demonstrating the impact of leakage and parasitics on performance.
   - Python scripts for parameter sensitivity analysis.
3. **`coupled_oscillators/`**Contains the implementation and simulation of ferroelectric-based coupled oscillators. This folder features:

   - SPICE files for relaxation oscillators based on the proposed model.
   - Synchronization dynamics of multiple oscillators.
   - Scripts for limit cycle projections and synchronization analysis.

## Key Features

- **Ferroelectric Model**: Implements a SPICE-compatible Landau-Khalatnikov equivalent positive feedback loop model.
- **Leakage and Parasitics**: Simulates real-world effects on ferroelectric behavior.
- **Coupled Oscillators**: Explores synchronization dynamics using the ferroelectric-based oscillator model.

## Getting Started

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. **Software Requirements**

   - **SPICE Simulator**: Compatible with tools like LTspice, HSPICE, or ngspice.
   - **Python**: Version 3.8 or higher for running analysis scripts.
   - Required Python Libraries: Install using
     ```bash
     pip install numpy matplotlib scipy
     ```
3. **Running Simulations**

   - **Single-domain model**: Navigate to `Fe_model/` and open `.sp` files directly in your SPICE simulator.
   - **Multi-domain simulation with Python**: Run the wrapper script:

   ```bash
     python Mult_dom_wrapper.py
   ```

This will:

- Generate a SPICE netlist (`fe_tanh_md.sp`) with multiple ferroelectric domains.
- Run SPICE simulations of P-V loops and transient dynamics.
- Automatically plot comparisons with experimental data.

## Python Wrapper for Multi-Domain Modeling

The file `Mult_dom_wrapper.py` provides an automated tool for generating and simulating multi-domain ferroelectric models, enabling statistical modeling and calibration with experimental data.

### Features

- **Domain Generation**: Assigns each domain a coercive voltage `Vc_i`, switching time `τ_i`, and saturation charge `Qo_i` using normal distributions.
- **Parameter Scaling**: Normalizes the total charge across domains so that ∑Qo_i = Qo. Charge is further distributed according to a power law on `Vc_i` to capture realistic domain switching behavior.
- **SPICE Netlist Output**: Generates a subcircuit-based SPICE model (`fe_tanh_md.sp`) where each domain instance is a modified version of the `fe_tanh` subcircuit. The overall circuit includes global parasitic resistance and capacitance.
  Example:

  ```spice
  .subckt fe_tanh_md in out
  XU_0 in out fe_tanh Vc=0.41 Qo=... tau=... K=2.62 off=-0.1
  ...
  Rp in out R=5e4
  Cp in out 0.19n
  .lib fe_tanh.sp
  .ends
  ```
- **Simulation Setup**: The wrapper also creates a testbench (`MD_sim.sp`) configured for:

  - P-V loop characterization using voltage sweeps.
  - Transient response to pulsed waveforms (e.g., PUND sequences).
- **Automated Analysis**: Simulations are executed via `Py2LTSpice.py`, and results are analyzed using NumPy and Pandas. The data are compared to measured results from `Data.xlsx`.
- **Visualization**: The wrapper generates overlay plots of simulation and experimental data, including:

  - Polarization-voltage (P-V) curves at different amplitudes.
  - Time-domain current and voltage responses.

### Customization

All modeling and simulation parameters are defined at the top of `Mult_dom_wrapper.py`, including:

- Number of domains.
- Statistical properties of `Vc`, `Qo`, and `τ`.
- Parasitic resistance and capacitance values.
- Experimental data sheet and plotting options.

## Citation

If you use this repository, please cite the paper:
**"An Optimized SPICE-Compatible Positive Feedback Model for Ferroelectric Devices: Design, Calibration, and Dynamic Simulations"**

## Contact

For questions or contributions, contact:
**Nicolás Villegas** (navillegas@miuandes.cl)
