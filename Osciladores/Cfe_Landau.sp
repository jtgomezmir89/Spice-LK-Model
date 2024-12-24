* Spice implementation of Landau


* Netlist Ferroelctric
.subckt Cfe_Landau in out s d PARAMS:
+Vc=0.4 Qo=0.08 K1=3.464 K2=0.385

Bref Fe 0 V=V(in,out)

*More negative move to right

.ic V(d)= -1
.ic V(s)= -1

Bs s 0 V=tanh(({K2}/{Vc})*(V(Fe)+{K1}*{Vc}*V(d))) ic = -1

Rd s d 70
Cd d 0 10e-6

Bi in out I=(ddt(({Qo}*V(d))))
.ends



