# Tool to quickly generate code to print text

from pyperclip import copy

string = input("> ")
locx = int(input("X Start location: "))
locy = int(input("Y Location: "))

if locx > 31 - len(string):
    raise ValueError("X too high!")
if locy > 7:
    raise ValueError("Y too high!")

loc = f'{locy:03b}{locx:05b}'

res = []

res.append("ldi x2 1\n")
res.append(f'ldi x1 {int(loc, 2):02x}h\n')
for i, char in enumerate(string):
    res.append(f'ldi x0 {ord(char):02x}h\n')
    if i != 0:
        res.append("add x1 x1 x2\n")
    res.append('int 1\n')

print(''.join(res))
copy(''.join(res))