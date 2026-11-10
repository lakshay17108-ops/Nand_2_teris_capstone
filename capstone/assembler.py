# assembler.py
# Hack assembler for Nand to Tetris I - Capstone Part B
# Name: Lakshay    Roll No: 2501730367   K = 67
#
# Usage:  python assembler.py Prog.asm
# Output: Prog.hack (16-bit binary lines) and symbols.txt
#
# Extra feature for my K (K mod 3 = 1):
#   save all labels and variables with their addresses in symbols.txt

import os
import sys

# ---------- tables ----------

COMP = {
    # a = 0
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    # a = 1  (same as above but with M instead of A)
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}

JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
for i in range(16):
    PREDEFINED["R" + str(i)] = i


# ---------- helpers ----------

def clean(line):
    """remove comment and all spaces from one line"""
    if "//" in line:
        line = line[:line.index("//")]
    return "".join(line.split())


def read_program(path):
    """first reading: drop comments / blank lines, record label addresses"""
    instructions = []
    labels = {}
    with open(path) as f:
        for raw in f:
            line = clean(raw)
            if line == "":
                continue
            if line.startswith("(") and line.endswith(")"):
                labels[line[1:-1]] = len(instructions)   # address of next instruction
            else:
                instructions.append(line)
    return instructions, labels


def dest_bits(dest):
    """d1 d2 d3 = A D M  (works for MD and DM, AM and MA, ...)"""
    bits = ""
    for letter in "ADM":
        bits += "1" if letter in dest else "0"
    return bits


def encode_a(value):
    return "0" + format(value, "015b")


def encode_c(line):
    dest = ""
    jump = ""
    comp = line
    if "=" in comp:
        dest, comp = comp.split("=", 1)
    if ";" in comp:
        comp, jump = comp.split(";", 1)
    return "111" + COMP[comp] + dest_bits(dest) + JUMP[jump]


def translate(instructions, labels):
    """second reading: turn every line into 16 bits"""
    symbols = dict(PREDEFINED)
    symbols.update(labels)
    variables = {}
    next_var = 16
    out = []
    for line in instructions:
        if line[0] == "@":
            name = line[1:]
            if name.isdigit():
                value = int(name)
            else:
                if name not in symbols:
                    symbols[name] = next_var
                    variables[name] = next_var
                    next_var += 1
                value = symbols[name]
            out.append(encode_a(value))
        else:
            out.append(encode_c(line))
    return out, variables


def write_symbols(path, labels, variables):
    with open(path, "w") as f:
        f.write("// labels\n")
        for name, addr in sorted(labels.items(), key=lambda x: x[1]):
            f.write("%s %d\n" % (name, addr))
        f.write("// variables\n")
        for name, addr in sorted(variables.items(), key=lambda x: x[1]):
            f.write("%s %d\n" % (name, addr))


def main():
    if len(sys.argv) < 2:
        print("usage: python assembler.py Prog.asm")
        return
    src = sys.argv[1]
    base = os.path.splitext(src)[0]
    out_dir = os.path.dirname(os.path.abspath(src))

    instructions, labels = read_program(src)
    binary, variables = translate(instructions, labels)

    with open(base + ".hack", "w") as f:
        f.write("\n".join(binary) + "\n")

    write_symbols(os.path.join(out_dir, "symbols.txt"), labels, variables)
    print("%s -> %s.hack  (%d instructions)" % (src, base, len(binary)))


if __name__ == "__main__":
    main()
