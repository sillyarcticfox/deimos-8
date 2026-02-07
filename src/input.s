ldi x2 1
ldi xf 7fh
.loop:
    int 2
    int 1
    add x1 x1 x2
    cmp x0 xf
    jmp.gt .loop
    jmp.lt .loop
hlt