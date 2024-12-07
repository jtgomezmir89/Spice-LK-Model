* Multi-domian dynamic SPICE Simulation
V1 in 0 PWL(0 0 0.5e-6 0 1.5e-6 -3 2.5e-6 -3 3.5e-6 0 4.5e-6 0 5.5e-6 -3 6.5e-6 -3 7.5e-6 0 8.5e-6 0 9.5e-6 2 10.5e-6 2 11.5e-6 0 12.5e-6 0 13.5e-6 3 14.5e-6 3 15.5e-6 0 16.5e-6 0 17.5e-6 3 18.5e-6 3 19.5e-6 0 20e-6 0)
Rsh 0 N0 1e-8
B1 Q 0 V=idt(-I(Rsh))
XU in N0 fe_tanh_md
.tran 0 20e-6 0.01e-6 1e-8
.lib C:\Users\MBX\Desktop\Investigacion\Spice-LK-Model\Fe_model\fe_tanh_md.sp
.backanno
.end
