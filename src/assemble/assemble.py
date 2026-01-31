"""
Assembles code for the Deimos-8 CPU.
Copyright (C) 2026  Sillyarcticfox

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import re, zlib, base64

def u8(n: int) -> int: return n & 0xFF
def u16(n: int) -> int: return n & 0xFFFF

memory = [0]*65536
registers = {"x0":0x0, "x1":0x1, "x2":0x2, "x3":0x3, "x4":0x4, "x5":0x5, "x6":0x6, "x7":0x7, "x8":0x8, "x9":0x9, "xa":0xa, "xb":0xb, "xc":0xc, "xd":0xd, "xe":0xe, "xf":0xf,
             "ex0":0x10, "ex1":0x11, "ex2":0x12, "ex3":0x13, "ex4":0x14, "ex5":0x15, "ex6":0x16, "ex7":0x17}
instruction_opcodes = {
    "nop": 0x00,
    "ldi": 0x01,
    "mov": 0x02,
    "btw": 0x03,
    "wtb": 0x04,
    "add": 0x05,
    "sub": 0x06,
    "mul": 0x07,
    "div": 0x08,
    "and": 0x09,
    "and.ext": 0x0A,
    "or": 0x0B,
    "or.ext": 0x0C,
    "inv": 0x0D,
    "xor": 0x0E,
    "xor.ext": 0x0F,
    "cmp": 0x10,
    "cmp.ext": 0x11,
    "jmp": 0x12,
    "jmp.ext": 0x13,
    "int": 0x14,
    "lod": 0x15,
    "str": 0x16,
    "hlt": 0x17,
}

def readf(fp: str) -> list[str]:
    with open(fp, "rt") as f:
        return [line.strip() for line in f.read().splitlines()]

def fmt(instrucs: list, start_offset: int = 0):
    known_labels = {}

    for i, instruc in enumerate(instrucs):
        instrucs[i] = [x.strip() for x in instruc.split(' ') if x.strip()]
        for j, inop in enumerate(instrucs[i]):
            if re.fullmatch(r'[0-9a-fA-F]+h', inop):
                instrucs[i][j] = u8(int(inop[:-1], 16))
            if inop.isnumeric():
                instrucs[i][j] = u8(int(inop, 10))
            if isinstance(inop, str) and inop.startswith('.') and inop.endswith(':'):
                known_labels[inop.replace(':', '')] = i * 5
                instrucs[i] = [-1]

    for i, instruc in enumerate(instrucs):
        if instruc == [-1]:
            continue

        for j, inop in enumerate(instruc):
            if isinstance(inop, int):
                continue
            elif inop in known_labels:
                instrucs[i][j] = known_labels[inop]
            elif inop in registers:
                instrucs[i][j] = registers[inop]
            elif inop in instruction_opcodes:
                instrucs[i][j] = instruction_opcodes[inop]
            else:
                suffix_map = {'.gt': 1, '.eq': 2, '.lt': 4}
                for suffix, value in suffix_map.items():
                    if inop.endswith(suffix):
                        base_op = inop[:-len(suffix)]
                        if base_op in registers:
                            instrucs[i][j] = registers[base_op]
                        elif base_op in instruction_opcodes:
                            instrucs[i][j] = instruction_opcodes[base_op]
                        else:
                            raise ValueError(f"Invalid operand before suffix: {inop}")
                        while len(instrucs[i]) < 5:
                            instrucs[i].append(0)
                        instrucs[i][4] = value
                        break
                else:
                    raise ValueError(f"Invalid operand: {inop}")

    instrucs = [instruc for instruc in instrucs if instruc != [-1] and instruc != ['']]

    for instruc in instrucs:
        instruc += [0] * (5 - len(instruc))

    flat = [0] * ((start_offset + 1) * 5) + [item for sublist in instrucs for item in sublist]

    return flat, instrucs

# Original code by __spetzers__. Changed it up quite a bit.
def list_to_huge_string(data):
    raw = bytearray()

    for value in data:
        if not (0 <= value <= 0xFFFF):
            raise ValueError(f"Value out of 16-bit range: {value}")
        
        raw.append(value & 0xFF)
        raw.append((value >> 8) & 0xFF)

    compressed = zlib.compress(raw, level=2, wbits=-15)
    encoded = base64.b64encode(compressed).decode("utf-8").strip("=")

    return encoded, data

if __name__ == '__main__':
    result = list_to_huge_string(fmt(readf("/home/arcticfox/Projects/deimos-8/src/assemble/input.s"))[0])
    print(result)
    print("Result written to ./out/asm_output.")
    with open("/home/arcticfox/Projects/deimos-8/out/asm_output", "wt") as f: f.write(result[0])