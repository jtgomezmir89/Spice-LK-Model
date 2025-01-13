Version 4
SymbolType BLOCK
RECTANGLE Normal -48 -24 64 24
WINDOW 3 8 24 Top 2
WINDOW 39 14 -92 Top 2
SYMATTR Value fe_tanh
SYMATTR SpiceLine Vc=1 Qo=1 K=2.62 tau=1e-9 off=0.5 rp=1e7 cp=1e-9
SYMATTR Prefix X
SYMATTR ModelFile ./fe_tanh_ni.sp
PIN -48 0 LEFT 8
PINATTR PinName in
PINATTR SpiceOrder 1
PIN 64 0 RIGHT 8
PINATTR PinName out
PINATTR SpiceOrder 2
