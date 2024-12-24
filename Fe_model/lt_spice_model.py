import Py2LTSpice
import paths
from subprocess import run
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid
import matplotlib.cm as cm


colormap = cm.get_cmap('winter')
def generate_model(domains, Vc_values, Qo_values, tau_values, offset, Parasitic_resistance, Parasitic_capacitance):

    with open("fe_tanh_md.sp", "w") as out:
        out.write("* Multi-domian SPICE model\n")
        
        out.write(".subckt fe_tanh_md in out\n")

        for i in range(0,domains):
            out.write("\n")
            out.write("*Grain_{0}:".format(i))
            out.write("\n")
            out.write("XU_"+str(i)+" in out fe_tanh Vc="+str(Vc_values[i])+" Qo="+str(Qo_values[i])+" K=2.62 tau="+str(tau_values[i])+" off="+str(offset))
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
        #out.write("V1 in 0 SINE(0 {0} 10 0 0 0 10)".format(Voltage))
        out.write("V1 in 0 PWL(0 0 0.025e-4 {0} 0.075e-4 -{0} 0.125e-4 {0} 0.175e-4 -{0} 0.2e-4 0)".format(Voltage))
        out.write("\n")
        out.write("Rsh 0 N0 1e-8")  
        out.write("\n")
        out.write("B1 Q 0 V=idt(-I(Rsh))")  
        out.write("\n") 
        out.write("XU in N0 fe_tanh_md")
        out.write("\n")
        out.write(".tran 0 0.25e-4 0 1e-8")     
        out.write("\n")
        out.write(r".lib C:\Users\MBX\Desktop\Investigacion\Spice-LK-Model\Fe_model\fe_tanh_md.sp")
        out.write("\n")
        out.write(".backanno")    
        out.write("\n")
        out.write(".end")
        out.write("\n")
    out.close()

def generate_sim_dyn():
    with open("MD_sim.sp", "w") as out:
        out.write("* Multi-domian dynamic SPICE Simulation\n")
        out.write("V1 in 0 PWL(0 0 0.5e-6 0 1.5e-6 -3 2.5e-6 -3 3.5e-6 0 4.5e-6 0 5.5e-6 -3 6.5e-6 -3 7.5e-6 0 8.5e-6 0 9.5e-6 2 10.5e-6 2 11.5e-6 0 12.5e-6 0 13.5e-6 3 14.5e-6 3 15.5e-6 0 16.5e-6 0 17.5e-6 3 18.5e-6 3 19.5e-6 0 20e-6 0)")
        out.write("\n")
        out.write("Rsh 0 N0 1e-8")  
        out.write("\n")
        out.write("B1 Q 0 V=idt(-I(Rsh))")  
        out.write("\n") 
        out.write("XU in N0 fe_tanh_md")
        out.write("\n")
        out.write(".tran 0 20e-6 0.01e-6 1e-8")     
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
    os.remove('MD_sim.raw')
    return data


def analyze_result(data, v, data_sim):
    data_sim[v]['time']={}
    data_sim[v]['in']={}
    data_sim[v]['q']={}
    data_sim[v]['i']={}

    for z in range(0,len(data['variables'])):
        expr = data['variables'][z][0]
        if expr=='time':
            data_sim[v]['time'] = abs(np.array(data['values'][:,z]))
        elif expr =='V(in)':
            data_sim[v]['in']=np.array(data['values'][:,z])
        elif expr =='V(q)':
            data_sim[v]['q']=np.array(data['values'][:,z])
        elif expr =='I(Rsh)':
            data_sim[v]['i']=np.array(data['values'][:,z])
    data_sim[v]['q']=data_sim[v]['q'] - (max(data_sim[v]['q']) + min(data_sim[v]['q'])) / 2
    return data_sim

def analyze_result_dyn(data, data_sim_dyn):
    data_sim_dyn['time']={}
    data_sim_dyn['in']={}
    data_sim_dyn['q']={}
    data_sim_dyn['i']={}

    for z in range(0,len(data['variables'])):
        expr = data['variables'][z][0]
        if expr=='time':
            data_sim_dyn['time'] = abs(np.array(data['values'][:,z]))
        elif expr =='V(in)':
            data_sim_dyn['in']=np.array(data['values'][:,z])
        elif expr =='V(q)':
            data_sim_dyn['q']=np.array(data['values'][:,z])
        elif expr =='I(Rsh)':
            data_sim_dyn['i']=np.array(data['values'][:,z])
    data_sim_dyn['q']=data_sim_dyn['q'] - (max(data_sim_dyn['q']) + min(data_sim_dyn['q'])) / 2
    return data_sim_dyn

def plot_data(data_sim, data_sim_dyn, voltages, df,df2, Area, skip):
    # Create a figure and define a grid layout for subplots
    fig = plt.figure(figsize=(10, 6))
    #gs = fig.add_gridspec(2, 2, width_ratios=[3, 3], height_ratios=[1, 1, 1], wspace=0.3, hspace=0.5)
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1], wspace=0.3, hspace=0.1)

    # Subplots on the left
    ax1 = fig.add_subplot(gs[0, 0])  # in vs time
    ax2 = fig.add_subplot(gs[1, 0])  # i vs time
    #ax3 = fig.add_subplot(gs[2, 0])  # q vs time

    # Single subplot on the right
    ax4 = fig.add_subplot(gs[:, 1:])  # q vs in

    # Plotting the data
    colors = [colormap(0), 'orangered', 'limegreen']
    c=0
    for v in voltages:
    #    ax1.plot(data_sim[v]['time']*1000, data_sim[v]['in'])
    #    ax2.plot(data_sim[v]['time']*1000, data_sim[v]['i'])
    #    ax3.plot(data_sim[v]['time']*1000, data_sim[v]['q'])
        ax4.plot(data_sim[v]['in'][skip:], 1e6*data_sim[v]['q'][skip:]/Area, '--', color=colors[c])
        c+=1
    
    ax4.plot(df['Vforce'], 1e6*df['Charge']/Area, label='0.5V', color=colors[0])
    ax4.plot(df['Vforce.1'], 1e6*df['Charge.1']/Area, label='1V', color=colors[1])
    #ax4.plot(df['Vforce.2'], 1e6*df['Charge.2']/Area, label='1.5V')
    ax4.plot(df['Vforce.3'], 1e6*df['Charge.3']/Area, label='2V', color=colors[2])
    ax4.plot(0, 0,'--', label='Sim.', color='k')
    ax4.plot(0, 0,'-', label='Meas.', color='k')


    ax1.plot(df2['TimeOutput.3']*1e6, df2['VMeasCh1.3'], color=colormap(0), label='Meas.')
    ax1.plot(data_sim_dyn['time']*1e6, data_sim_dyn['in'], color='orangered', linestyle='--', label='Sim.')
    ax2.plot(df2['TimeOutput.3']*1e6, df2['IMeasCh1.3']*1000, color=colormap(0))
    ax2.plot(data_sim_dyn['time']*1e6, -1*data_sim_dyn['i']*1000, color='orangered', linestyle='--')
    #charge = cumulative_trapezoid(df2['IMeasCh1.3'], df2['TimeOutput.3'], initial=0) 


    #ax3.plot(df2['TimeOutput.3']*1e6, 1e6*charge/Area)
    #ax3.plot(data_sim_dyn['time']*1e6, 1e6*(data_sim_dyn['q']-data_sim_dyn['q'][0])/Area)
    ax1.set_title("PUND Calibration", fontsize=20)
    #ax1.set_xlabel("Time [$\mu s$]")
    ax1.set_ylabel("Voltage [V]", fontsize=15)
    ax2.set_xlabel("Time [$\mu s$]", fontsize=15)
    ax2.set_ylabel("Current [mA]", fontsize=15)

    #ax4.plot(data_sim['in'], data_sim['q'], label="SPICE", color='red')
    ax4.set_title("P-V Calibration", fontsize=20)
    ax1.legend(fontsize=15)

    ax4.set_xlabel("Voltage [V]", fontsize=15)
    ax4.set_ylabel("Polarization [$\mu C$ / $cm^2$]", fontsize=15)
    ax4.legend(fontsize=15)
    ax1.tick_params(axis='x', labelsize=0)
    ax1.tick_params(axis='y', labelsize=15)
    ax2.tick_params(axis='x', labelsize=15)
    ax2.tick_params(axis='y', labelsize=15)
    ax4.tick_params(axis='x', labelsize=15)
    ax4.tick_params(axis='y', labelsize=15)
    ax1.grid(True)
    ax2.grid(True)
    ax4.grid(True)
    # Show the plot
    plt.tight_layout()
    plt.show()