* Spice implementation of Landau


* Netlist Ferroelctric
.subckt fe_tanh in out ql qn qt PARAMS:
+Vc=1 Qo=1 K=2.598076211353316

.ic V(ql)= 0
.ic V(qn)= 0
.ic V(qt)= 0

Bref n 0 V=V(in,out)/{Vc}

Bl ql 0 V=(V(n)/(3*{K}))+(4/3)*V(qn)
Rd ql qt 40
Cd qt 0 10e-7
Bn qn 0 V=tanh(V(qt))
Bi in out I=(ddt(({Qo}*V(qn))))
.ends



