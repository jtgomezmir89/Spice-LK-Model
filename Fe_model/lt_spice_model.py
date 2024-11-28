import Py2LTSpice

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
            out.write("XU_{0} in N0 fe_tanh Vc={1} Qo={2} K=2.62 tau={2}".format(i, Vc_values[i],Qo_values[i], tau_values[i]))
            out.write("\n")

        out.write(".tran 0 1.5m 0 1e-9")  
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


    return 


def analyze_result():

    results=1
    return results 
