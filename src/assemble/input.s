ldi x3 7fh
ldi x2 1
ldi x0 65
ldi x1 0
int 1
cmp x0 x3
add x0 x0 x2
add x1 x1 x2
int 1
jmp.gt 30
jmp.lt 30
ldi x0 ffh
int 1
hlt