# An Optimized SPICE-Compatible Positive Feedback Model for Ferroelectric Devices

This repository contains the simulation files for reproducing and extending the results presented in the paper:

**"An Optimized SPICE-Compatible Positive Feedback Model for Ferroelectric Devices: Design, Calibration, and Dynamic Simulations"**  
Authors: Nicolás Villegas, Joaquín Carvajal, Shumiya Alam, Tanvir Pantha, Jaime Cisternas, Kai Ni, Sourav Dutta, Jorge Gómez

## Repository Structure

The repository is organized into the following directories:

1. **`Fe_model/`**  
   Contains the SPICE-compatible single-domain ferroelectric model. This folder includes:
   - SPICE netlists for the Landau-Khalatnikov (L-K) equivalent model.
   - Calibration scripts for static and dynamic behavior.
   - Example simulations for polarization-voltage (P-V) and polarization switching dynamics.

2. **`Fe_leakage_model/`**  
   Includes an extended version of the ferroelectric model with leakage current and parasitic capacitance. This folder provides:
   - Circuit files accounting for non-idealities in ferroelectric capacitors.
   - Simulations demonstrating the impact of leakage and parasitics on performance.
   - Python scripts for parameter sensitivity analysis.

3. **`coupled_oscillators/`**  
   Contains the implementation and simulation of ferroelectric-based coupled oscillators. This folder features:
   - SPICE files for relaxation oscillators based on the proposed model.
   - Synchronization dynamics of multiple oscillators.
   - Scripts for limit cycle projections and synchronization analysis.

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
   - Navigate to the desired folder (e.g., `Fe_model/`) and open the SPICE netlist in your simulator.
   - For Python-based analysis, run scripts directly in the folder, e.g.,  
     ```bash
     python analyze_static_response.py
     ```

## Key Features

- **Ferroelectric Model**: Implements a SPICE-compatible Landau-Khalatnikov equivalent positive feedback loop model.
- **Leakage and Parasitics**: Simulates real-world effects on ferroelectric behavior.
- **Coupled Oscillators**: Explores synchronization dynamics using the ferroelectric-based oscillator model.

## Citation

If you use this repository, please cite the paper:  
**"An Optimized SPICE-Compatible Positive Feedback Model for Ferroelectric Devices: Design, Calibration, and Dynamic Simulations"**

## Contact

For questions or contributions, contact:
**Nicolás Villegas** (navillegas@miuandes.cl)
