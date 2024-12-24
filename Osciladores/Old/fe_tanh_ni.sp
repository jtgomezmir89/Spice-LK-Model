* Spice implementation of Landau


* Netlist Ferroelctric
.subckt fe_tanh in out PARAMS:
+Vc=1 Qo=1 K=2.62 tau=1e-9 off=0.5 rp=1e7 cp=1e-9

Bref n 0 V=(V(in)-{off}-V(out))/{Vc}
Bl ql 0 V=V(n)+{K}*V(qn)ic=-1
Rd ql qt R={{tau}/1e-9}
Cd qt 0 1e-9 ic=-1
Bn qn 0 V=tanh(V(qt))
Bi in out I=(ddt(({Qo}*V(qn))))
Rp in out R={rp}
Cp in out {cp}
.ends



