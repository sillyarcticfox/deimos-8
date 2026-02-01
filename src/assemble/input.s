ldi x0 44h
ldi x1 0
int 1
ldi x0 65h
ldi x1 1
int 1
ldi x0 69h
ldi x1 2
int 1
ldi x0 6dh
ldi x1 3
int 1
ldi x0 4fh
ldi x1 4
int 1
ldi x0 53h
ldi x1 5
int 1
ldi x1 0
ldi x2 1h
.ram_check:
    ldi x0 52h
    ldi x1 20h
    int 1
    ldi x0 41h
    add x1 x1 x2
    int 1
    ldi x0 4dh
    add x1 x1 x2
    int 1
    ldi x0 43h
    add x1 x1 x2
    int 1
    ldi x0 48h
    add x1 x1 x2
    int 1
    ldi x0 45h
    add x1 x1 x2
    int 1
    ldi x0 43h
    add x1 x1 x2
    int 1
    ldi x0 4bh
    add x1 x1 x2
    int 1
    ldi x0 2eh
    add x1 x1 x2
    int 1
    ldi x0 2eh
    add x1 x1 x2
    int 1
    ldi x0 2eh
    add x1 x1 x2
    int 1
    ldi x0 20h
    add x1 x1 x2
    int 1
    mov x7 x1

    ldi x4 1
    ldi x5 7fh
    ldi x6 ffh
    btw ex0 x5 x6
    ldi x0 afh
    ldi x1 77h
    str ex0 x0
    add x5 x5 x4
    ldi x6 0
    btw ex0 x5 x6
    str ex0 x1
    lod ex0 x3
    ldi x5 7fh
    ldi x6 ffh
    btw ex0 x5 x6
    lod ex0 x2

    cmp x0 x2
    jmp.gt .rcerr
    jmp.lt .rcerr
    cmp x1 x3
    jmp.gt .rcerr
    jmp.lt .rcerr

    ldi x2 1
    mov x1 x7

    ldi x0 4fh
    add x1 x1 x2
    int 1
    ldi x0 4bh
    add x1 x1 x2
    int 1
    
    jmp .bootload

.bootload:
    ldi x2 0
    ldi x3 0
    ldi x4 0
    ldi x5 0
    ldi x6 0
    ldi x7 0
    ldi x8 0
    ldi x9 0
    ldi xa 0
    ldi xb 0
    ldi xc 0
    ldi xd 0
    ldi xe 0
    ldi xf 0
    ldi ex0 0
    ldi ex1 0
    ldi ex2 0
    ldi ex3 0
    ldi ex4 0
    ldi ex5 0
    ldi ex6 0

    ldi x0 81h
    ldi x1 00h
    btw ex7 x0 x1
    mov ex6 ex7

    ldi x0 0
    ldi x1 0

    jmp .kstartsplash

.rcerr:
    ldi xf 01h
    ldi x2 1
    mov x1 x7
    ldi x0 45h
    add x1 x1 x2
    int 1
    ldi x0 52h
    add x1 x1 x2
    int 1
    ldi x0 52h
    add x1 x1 x2
    int 1
    ldi x0 4fh
    add x1 x1 x2
    int 1
    ldi x0 52h
    add x1 x1 x2
    int 1
    hlt

.kstartsplash:
    ldi x0 ffh
    int 1

    ldi x2 1
    ldi x1 00h
    ldi x0 44h
    int 1
    ldi x0 65h
    add x1 x1 x2
    int 1
    ldi x0 69h
    add x1 x1 x2
    int 1
    ldi x0 6dh
    add x1 x1 x2
    int 1
    ldi x0 4fh
    add x1 x1 x2
    int 1
    ldi x0 53h
    add x1 x1 x2
    int 1
    ldi x0 20h
    add x1 x1 x2
    int 1
    ldi x0 6bh
    add x1 x1 x2
    int 1
    ldi x0 65h
    add x1 x1 x2
    int 1
    ldi x0 72h
    add x1 x1 x2
    int 1
    ldi x0 6eh
    add x1 x1 x2
    int 1
    ldi x0 65h
    add x1 x1 x2
    int 1
    ldi x0 6ch
    add x1 x1 x2
    int 1
    ldi x0 20h
    add x1 x1 x2
    int 1
    ldi x0 73h
    add x1 x1 x2
    int 1
    ldi x0 74h
    add x1 x1 x2
    int 1
    ldi x0 61h
    add x1 x1 x2
    int 1
    ldi x0 72h
    add x1 x1 x2
    int 1
    ldi x0 74h
    add x1 x1 x2
    int 1
    ldi x0 69h
    add x1 x1 x2
    int 1
    ldi x0 6eh
    add x1 x1 x2
    int 1
    ldi x0 67h
    add x1 x1 x2
    int 1
    ldi x0 2eh
    add x1 x1 x2
    int 1
    ldi x0 2eh
    add x1 x1 x2
    int 1
    ldi x0 2eh
    add x1 x1 x2
    int 1
    ldi x0 ffh
    int 1

    ldi x1 0

    ldi xe 8

    jmp .kstart

.kstart:
    int 2
    cmp x0 xe
    jmp.eq .bs
    int 1
    add x1 x1 x2
    jmp .kstart
.bs:
    ldi x0 0
    sub x1 x1 x2
    int 1
    jmp .kstart