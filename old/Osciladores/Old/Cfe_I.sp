

.subckt Cfe_I in out s c q p cap PARAMS:
+ Qf=100p Cs=2p Vup=0.3 Vdw=-0.3


* Initial conditions:
.ic V(s)= 1
.ic V(c)= 1


Ep p out value={Vdw*(1-V(s))+Vup*V(s)} ic = Vup
Es s 0 value={0.5*(1+tanh(1000000*(V(p)-V(in))))} ic=1
Rq s c 50k
Cq c 0 50p
Eq q 0 value={Qf*(1-V(c))+Cs*V(in,out)}
Bcap cap 0 V=ddt(V(q))/ddt(V(in,out))
Bi in out I=ddt(V(q))

.ends
