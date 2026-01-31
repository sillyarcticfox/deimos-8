from assemble import fmt, readf, u8, u16 #type:ignore #I don't know why vscode thinks fmt and readf don't exist
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
registers['gt'] = 0
registers['eq'] = 1
registers['lt'] = 0

memory = [0] * 65536 # Memory
clockspeed = int(input("Clock frequency (Hz): ")) # Clock frequency

program = fmt(readf("/home/arcticfox/Projects/deimos-8/src/assemble/input.s"))
print("PROGRAM:", program[1])

for i, inop in enumerate(program[0]):
    memory[i] = inop

halted = False

while not halted:
    try: time.sleep(1 / clockspeed)
    except ZeroDivisionError: ...
        
    for i in range(5):
        try:
            registers[f'ir{i}'] = memory[registers['pc']+i]
        except IndexError:
            print("Program counter overflow, halting.")
            halted = True
    print(registers['ir0'], registers['ir1'], registers['ir2'], registers['ir3'], registers['ir4'], dict(list(registers.items())[:24]))

    cond = True

    match registers['ir4']:
        case 1: cond = bool(registers['gt'])
        case 2: cond = bool(registers['eq'])
        case 3: cond = bool(registers['lt'])

    if cond:
        match registers['ir0']:
            case 0: ...
            case 1: # ldi
                registers[registers['ir1']] = u8(registers['ir2'])
            case 2: # mov
                registers[registers['ir1']] = registers[registers['ir2']] 
            case 3: # btw
                if registers['ir1'] < 16:
                    print("Byte to word destination must be a 16-bit register, halting.")
                    halted = True
                registers[registers['ir1']] = ((registers[registers['ir2']] << 8) | registers[registers['ir3']])
            case 5: # add
                registers[registers['ir1']] = u8(registers[registers['ir2']] + registers[registers['ir3']])
            case 6: # sub
                registers[registers['ir1']] = u8(registers[registers['ir2']] - registers[registers['ir3']])
            case 7: # mul
                if registers['ir1'] < 16:
                    print("Multiplication destination must be a 16-bit register, halting.")
                    halted = True
                registers[registers['ir1']] = u16(registers[registers['ir2']] * registers[registers['ir3']])
            case 8: # div
                registers[registers['ir1']] = u8(round(registers[registers['ir2']] / registers[registers['ir3']]))
            case 16: # cmp
                registers['gt'] = False
                registers['eq'] = False
                registers['lt'] = False
                if u8(registers[registers['ir1']]) > u8(registers[registers['ir2']]):
                    registers['gt'] = True
                elif u8(registers[registers['ir1']]) == u8(registers[registers['ir2']]):
                    registers['eq'] = True
                elif u8(registers[registers['ir1']]) < u8(registers[registers['ir2']]):
                    registers['lt'] = True
            case 21: # hlt
                halted = True
            case _:
                print("Opcode invalid, halting.")
                halted = True

    registers['pc'] += 5

print("\n==========================================================================================================\n\nREGISTER DUMP:", registers)