Version 4
SymbolType BLOCK
RECTANGLE Normal -32 -40 32 40
WINDOW 3 115 -34 Top 2
WINDOW 39 232 -14 Top 2
SYMATTR Value transistor
SYMATTR SpiceLine K=1100u lambda=0.1 Vt=0.7
SYMATTR Prefix X
SYMATTR ModelFile ./transistor.sp
PIN -32 0 LEFT 8
PINATTR PinName g
PINATTR SpiceOrder 1
PIN 16 -48 VRIGHT 8
PINATTR PinName d
PINATTR SpiceOrder 2
PIN 16 48 VLEFT 8
PINATTR PinName s
PINATTR SpiceOrder 3
