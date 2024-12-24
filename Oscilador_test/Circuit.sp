
XU1 g Vdd s transistor K=1100u lambda=0.1 Vt=0.7
V1 Vdd 0 3.3
V2 in 0 1
XU2 in g N001 N002 N003 N004 N005 Cfe_I Qf=22p Cs=1p Vup=-0.19 Vdw=-0.65
C1 Vdd g 23p
C2 g s 80p
R1 Vdd g 1e50
R2 g s 1e50
R3 g in 1e50
I1 s 0 0.39µ
C3 s 0 0.1µ
.tran 0 0.5 0 50n startup
.ic V(g)=0 V(s)=0
.lib Cfe_I.sp
.lib transistor.sp
.backanno
.end
