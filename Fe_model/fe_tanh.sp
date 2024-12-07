* Spice implementation of Landau


* Netlist Ferroelctric
.subckt fe_tanh in out PARAMS:
+Vc=1 Qo=1 K=2.62 tau=1e-9 off=-0.5

Bref n 0 V=(V(in)-{off}-V(out))/{Vc}
Bl ql 0 V=V(n)+{K}*V(qn)
Rd ql qt R={{tau}/1e-9}
Cd qt 0 1e-9
Bn qn 0 V=tanh(V(qt))
Bi in out I=(ddt(({Qo}*V(qn))))
.ends



