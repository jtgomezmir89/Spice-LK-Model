* Spice implementation of Landau


* Netlist Ferroelctric
.subckt fe_tanh in out ql qn qt PARAMS:
+Vc=1 Qo=1 K=2.6

Bref n 0 V=V(in,out)/{Vc}
Bl ql 0 V=V(n)+{K}*V(qn)
Rd ql qt 10
Cd qt 0 10e-7
Bn qn 0 V=tanh(V(qt))
Bi in out I=(ddt(({Qo}*V(qn))))
.ends



