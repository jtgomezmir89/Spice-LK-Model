import Py2LTSpice
import paths
from subprocess import run
import os
import numpy as np
import matplotlib.pyplot as plt

def generate_model(domains, Vc_values, Qo_values, tau_values, Parasitic_resistance, Parasitic_capacitance):

    with open("MD_Model.sp", "w") as out:
        out.write("* Multi-domian SPICE model\n")
        
        out.write(".subckt fe_tanh_md in out\n")

        for i in range(0,domains):
            out.write("\n")
            out.write("*Grain_{0}:".format(i))
            out.write("\n")
            out.write("XU_"+str(i)+" in out fe_tanh Vc="+str(Vc_values[i])+" Qo="+str(Qo_values[i])+" K=2.62 tau="+str(tau_values[i]))
            out.write("\n")
        out.write("Rp in out R="+str(Parasitic_resistance))
        out.write("\n") 
        out.write("Cp in out "+str(Parasitic_capacitance)) 
        out.write("\n")
        out.write(r".lib C:\Users\MBX\Desktop\Investigacion\Spice-LK-Model\Fe_model\fe_tanh.sp")
        out.write("\n")
        out.write(".ends")
        out.write("\n")
    out.close()


def generate_sim(Voltage):
    with open("MD_sim.sp", "w") as out:
        out.write("* Multi-domian SPICE Simulation\n")
        out.write("V1 in 0 SINE(0 2.1 1k 0 0 0 10)".format(Voltage))
        out.write("\n")
        out.write("Rsh 0 N0 0.00000001")  
        out.write("\n")
        out.write("B1 Q 0 V=idt(-I(Rsh))")  
        out.write("\n") 
        out.write("XU in N0 fe_tanh_md")
        out.write(".tran 0 1.5m 0 1e-8")     
        out.write("\n")
        out.write(r".lib C:\Users\MBX\Desktop\Investigacion\Spice-LK-Model\Fe_model\fe_tanh_md.sp")
        out.write("\n")
        out.write(".backanno")    
        out.write("\n")
        out.write(".end")
        out.write("\n")
    out.close()


def run_spice():
    run(paths.spice_path+' -b -Run MD_sim.sp')
    data = Py2LTSpice.read_ltspice_raw('MD_sim.raw')
    #os.remove('MD_Model.raw')
    return data


def analyze_result(data, data_sim):
    data_sim['time']={}
    data_sim['in']={}
    data_sim['q']={}
    data_sim['i']={}

    for v in range(0,len(data['variables'])):
        expr = data['variables'][v][0]
        if expr=='time':
            data_sim['time'] = abs(np.array(data['values'][:,v]))
        elif expr =='V(in)':
            data_sim['in']=np.array(data['values'][:,v])
        elif expr =='V(q)':
            data_sim['q']=np.array(data['values'][:,v])
        elif expr =='I(Rsh)':
            data_sim['i']=np.array(data['values'][:,v])
    return data_sim

def plot_data(data_sim, df, Area):
    # Create a figure and define a grid layout for subplots
    fig = plt.figure(figsize=(10, 6))
    gs = fig.add_gridspec(3, 2, width_ratios=[3, 3], height_ratios=[1, 1, 1], wspace=0.3, hspace=0.5)

    # Subplots on the left
    ax1 = fig.add_subplot(gs[0, 0])  # in vs time
    ax2 = fig.add_subplot(gs[1, 0])  # i vs time
    ax3 = fig.add_subplot(gs[2, 0])  # q vs time

    # Single subplot on the right
    ax4 = fig.add_subplot(gs[:, 1:])  # q vs in

    # Plotting the data
    ax1.plot(data_sim['time']*1000, data_sim['in'], label="SPICE")
    ax1.set_xlabel("Time [ms]")
    ax1.set_ylabel("Voltage [V]")
    ax1.legend()

    ax2.plot(data_sim['time']*1000, data_sim['i'], label="SPICE", color='orange')
    ax2.set_xlabel("Time [ms]")
    ax2.set_ylabel("Current [A]")
    ax2.legend()

    ax3.plot(data_sim['time']*1000, data_sim['q'], label="SPICE", color='green')
    ax3.set_xlabel("Time [ms]")
    ax3.set_ylabel("Charge [C]")
    ax3.legend()

    #ax4.plot(data_sim['in'], data_sim['q'], label="SPICE", color='red')

    ax4.plot(df['Vforce'], 1e6*df['Charge']/Area, label='0.5V')
    ax4.plot(df['Vforce.1'], 1e6*df['Charge.1']/Area, label='1V')
    ax4.plot(df['Vforce.2'], 1e6*df['Charge.2']/Area, label='1.5V')
    ax4.plot(df['Vforce.3'], 1e6*df['Charge.3']/Area, label='2V')


    ax4.legend()


    ax4.set_xlabel("Voltage [V]")
    ax4.set_ylabel("Polarization [$\mu C$/$cm^2$]")
    ax4.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()