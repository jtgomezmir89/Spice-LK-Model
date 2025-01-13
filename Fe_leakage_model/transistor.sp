

.subckt transistor g d s PARAMS:
+ K=1100u lambda=0.1 Vt=0.7



Eds ds 0 value={V(d)-V(s)}
Egs gs 0 value={V(g)-V(s)}
Eov ov 0 value={V(gs)-Vt}

Eoff off 0 value={1n}
Elin lin 0 value={K*(V(ov)*V(ds)-square(V(ds))/2)*(1+lambda*V(ds))}
Esat sat 0 value={(K/2)*(square(V(ov)))*(1+lambda*V(ds))}

Bi d s I=if(V(gs)<=Vt,V(off),if(V(ds)<=V(ov),V(lin),V(sat)))

.ends
