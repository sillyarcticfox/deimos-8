from assemble import fmt, readf #type:ignore #I don't know why vscode thinks fmt and readf don't exist
from assemble import registers as register_to_int #type:ignore 
import time

# Python 3.7+ required

registers = {}
for i in register_to_int.values():
    registers[i] = 0
registers['ir0'] = 0
registers['ir1'] = 0
registers['ir2'] = 0
registers['ir3'] = 0
registers['ir4'] = 0
registers['pc'] = 0

memory = [0] * 65536 # Memory
clockspeed = int(input("Clock frequency (Hz): ")) # Clock frequency

program = fmt(readf("/home/arcticfox/Projects/deimos-8/src/assemble/input.s"))
print("PROGRAM:", program[1])

for i, inop in enumerate(program[0]):
    memory[i] = inop

halted = False

while not halted:
    time.sleep(1 / clockspeed)
    for i in range(5):
        registers[f'ir{i}'] = memory[registers['pc']+i]
    print(registers['ir0'], registers['ir1'], registers['ir2'], registers['ir3'], registers['ir4'], dict(list(registers.items())[:24]))
    match registers['ir0']:
        case 0: ...
        case 1: # ldi
            registers[registers['ir1']] = registers['ir2']
        case 5: # add
            registers[registers['ir1']] = registers[registers['ir2']] + registers[registers['ir3']]
        case 21: # hlt
            halted = True
        case _:
            print("Opcode invalid, halting.")
            halted = True

    registers['pc'] += 5

print("REGISTER DUMP:", registers)