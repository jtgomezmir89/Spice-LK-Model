import Py2LTSpice
import paths
from subprocess import run
import os
import numpy as np

def generate_model(domains, Vc_values, Qo_values, tau_values ):


    with open("MD_Model.sp", "w") as out:
        out.write("* Multi-domian SPICE model\n")

        out.write("V1 in 0 SINE(0 2.1 1k 0 0 0 10)")
        out.write("\n")
        out.write("Rsh 0 N0 0.00000001")  
        out.write("\n")
        out.write("B1 Q 0 V=idt(-I(Rsh))")  
        out.write("\n") 
 
        for i in range(0,domains):
            out.write("\n")
            out.write("*Grain_{0}:".format(i))
            out.write("\n")
            out.write("XU_"+str(i)+" in N0 fe_tanh Vc="+str(Vc_values[i])+" Qo="+str(Qo_values[i])+" K=2.62 tau="+str(tau_values[i]))
            out.write("\n")

        out.write(".tran 0 1.5m 0 1e-8")  
        out.write("\n")    
        out.write("\n")
        out.write(r".lib C:\Users\MBX\Desktop\Investigacion\Spice-LK-Model\Fe_model\fe_tanh.sp")
        out.write("\n")
        out.write(".backanno")    
        out.write("\n")
        out.write(".end")
        out.write("\n")
    out.close()



def run_spice():
    run(paths.spice_path+' -b -Run MD_Model.sp')
    data = Py2LTSpice.read_ltspice_raw('MD_Model.raw')
    #os.remove('MD_Model.raw')
    return data


def analyze_result(data):

    data_sim={}
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
