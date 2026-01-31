from assemble import fmt, readf, u8, u16 #type:ignore #I don't know why vscode thinks fmt and readf don't exist
from assemble import registers as register_to_int #type:ignore
import time

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
registers['eq'] = 0
registers['lt'] = 0

memory = [0] * 65536 # Memory
tty = [''] * 256 # TTY Memory

program = fmt(readf("/home/arcticfox/Projects/deimos-8/src/assemble/input.s"))
print("PROGRAM:", program[1])

clockspeed = int(input("Clock frequency (Hz): ")) # Clock frequency
ttymode = input("TTY Mode? (y/N) ") # TTY Mode

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
    if ttymode != 'y':
        print(registers['ir0'], registers['ir1'], registers['ir2'], registers['ir3'], registers['ir4'], dict(list(registers.items())[:24]))


    cond = True

    match registers['ir4']:
        case 1: cond = bool(registers['gt'])
        case 2: cond = bool(registers['eq'])
        case 4: cond = bool(registers['lt'])

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
            case 4: # wtb
                registers[registers['ir1']] = (registers[registers['ir3']] >> 8) & 0xff
                registers[registers['ir2']] = registers[registers['ir3']] & 0xff
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
            case 9: # and
                registers[registers['ir1']] = u8(registers[registers['ir2']] & registers[registers['ir3']])
            case 10: # and.ext
                if registers['ir1'] < 16 or registers['ir2'] < 16 or registers['ir3'] < 16:
                    print("Extended bitwise needs all 3 operands to be extended registers, halting.")
                    halted = True
                registers[registers['ir1']] = u16(registers[registers['ir2']] & registers[registers['ir3']])
            case 11: # or
                registers[registers['ir1']] = u8(registers[registers['ir2']] | registers[registers['ir3']])
            case 12: # or.ext
                if registers['ir1'] < 16 or registers['ir2'] < 16 or registers['ir3'] < 16:
                    print("Extended bitwise needs all 3 operands to be extended registers, halting.")
                    halted = True
                registers[registers['ir1']] = u16(registers[registers['ir2']] | registers[registers['ir3']])
            case 13: # inv
                registers[registers['ir1']] = u8(~(registers[registers['ir2']]))
            case 14: # xor
                registers[registers['ir1']] = u8(registers[registers['ir2']] ^ registers[registers['ir3']])
            case 15: # xor.ext
                if registers['ir1'] < 16 or registers['ir2'] < 16 or registers['ir3'] < 16:
                    print("Extended bitwise needs all 3 operands to be extended registers, halting.")
                    halted = True
                registers[registers['ir1']] = u16(registers[registers['ir2']] ^ registers[registers['ir3']])
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
            case 18: # jmp
                registers['pc'] = registers['ir1']
                continue
            case 19: # jmp.ext
                registers['pc'] = ((registers[registers['ir1']] << 8) | registers[registers['ir2']])
                continue
            case 20: # int
                match registers['ir1']:
                    case 1:
                        if registers[0] == 255:
                            tty = [''] * 256
                        else:
                            tty[registers[1]] = chr(registers[0])
                    case 2:
                        key = input("> ")
                        if len(key) != 1:
                            print("Input must be 1 character exactly, halting.")
                            halted = True
                        registers[0] = ord(key)
                    case _:
                        print("Interrupt not implemented, halting.")
                        halted = True
            case 21: # lod
                registers[registers['ir2']] = memory[registers[registers['ir1']]]
            case 22: # str
                memory[registers[registers['ir1']]] = registers[registers['ir2']]
            case 23: # hlt
                halted = True
            case _:
                print("Opcode invalid, halting.")
                halted = True

    if ttymode == 'y':
        for row in range(8):
            start = row * 32
            end = start + 32
            print("".join(tty[start:end]))
        print("".join(['=']*32))
    registers['pc'] += 5

print("\n==========================================================================================================\n\nREGISTER DUMP:\n")

for k, v in registers.items():
    try:
        int(k)
        if k < 16: k = f'x{hex(k).replace('0x', '')}'
        else: k = f'ex{hex(k-16).replace('0x', '')}'
    except ValueError: ...
    print(k, ':', hex(v).replace('0x', '')+'h')


with open("/home/arcticfox/Projects/deimos-8/out/MEMDUMP", "w") as f:
    for i in range(0, len(memory), 16):
        line = memory[i:i+16]
        f.write(" ".join(map(str, line)) + "\n")