* Multi-domian SPICE model
V1 in 0 PULSE(0 1 1.2u 0.5u 0.5u 0.5u 2u 1)
B1 Q 0 V=idt(-I(V1))

*Grain_0:
Rq_0 in ini_0 0.001

Br_0 Qr_0 0 V=idt(I(Rq_0))

*Grain_1:
Rq_1 in ini_1 0.001

Br_1 Qr_1 0 V=idt(I(Rq_1))

*Grain_2:
Rq_2 in ini_2 0.001

Br_2 Qr_2 0 V=idt(I(Rq_2))

*Grain_3:
Rq_3 in ini_3 0.001

Br_3 Qr_3 0 V=idt(I(Rq_3))

*Grain_4:
Rq_4 in ini_4 0.001

Br_4 Qr_4 0 V=idt(I(Rq_4))

*Grain_5:
Rq_5 in ini_5 0.001

Br_5 Qr_5 0 V=idt(I(Rq_5))

*Grain_6:
Rq_6 in ini_6 0.001

Br_6 Qr_6 0 V=idt(I(Rq_6))

*Grain_7:
Rq_7 in ini_7 0.001

Br_7 Qr_7 0 V=idt(I(Rq_7))

*Grain_8:
Rq_8 in ini_8 0.001

Br_8 Qr_8 0 V=idt(I(Rq_8))

*Grain_9:
Rq_9 in ini_9 0.001

Br_9 Qr_9 0 V=idt(I(Rq_9))

.tran 0 3.8u 0.8u 0.2n
.lib C:\Users\jtgom\Google Drive\JxCDC\Multidomain\Cfe_Landau.sp
.end
