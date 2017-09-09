#!/usr/bin/env python3
import re

str_ops = {
    "noop": 0x00,
    "drop": 0x01,
    "load": 0x02,
    "dup" : 0x03,
    "swap": 0x04,
    "over": 0x05,
    "rot" : 0x06,
    "nip" : 0x07,
    "tuck": 0x08,

    "add": 0x09,
    "inc": 0x0A,
    "dec": 0x0B,
    "sub": 0x0C,
    "mul": 0x0D,
    "div": 0x0E,
    "mod": 0x0F,

    "jump": 0x10,
    "eqjp": 0x11,
    "gtjp": 0x12,
    "ltjp": 0x13,
    "eqzjp": 0x14,
    "gtzjp": 0x15,
    "ltzjp": 0x16,

    "in" : 0x17,
    "out": 0x18
}


def cleanup(text):
    text = re.sub(r';.*', '', text)
    ops = re.split(r'[ \n]+', text)
    ops = filter(lambda x: x, ops)
    return list(ops)


def asm(filename):
    with open(filename, "r") as file:
        text = file.read()
    ops = cleanup(text)

    routine = { "data": None, "ins": None }
    if "DAT" not in ops:
        raise Exception("All programs must begin with a data sector. " + \
                        "Even if empty.")
    if "INS" not in ops:
        raise Exception("Instruction sector is missing.")
    else:
        ins_start = ops.index("INS")
    routine["data"] = list(map(int, ops[1:ins_start]))

    labels = {}
    refs = []
    ip = 0
    ops = ops[ins_start+1:]
    while ip != len(ops):
        op = ops[ip]
        # check if label and remember position
        if op[-1] == ":":
            labels[(op[:-1])] = ip
            ops.pop(ip - len(ops))
            ip += 0
        # check if reference, and mark in refs
        elif op[0] == "@":
            ops[ip] = op[1:]
            refs.append(ip)
            ip += 1
        # check if opcode and turn to code
        elif op in str_ops:
            ops[ip] = str_ops[op]
            ip += 1
        # else, it's an int
        else:
            ops[ip] = int(op)
            ip += 1
    # turn references to actual locations
    for ref in refs:
        ops[ref] = labels[ops[ref]]
    routine["ins"] = ops
    return routine


def hexit(num, no_bytes=8):
    byte = []
    while num != 0:
        rem = num % 256
        num //= 256
        byte.append(rem)
    while len(byte) != no_bytes:
        byte.append(0)
    return bytes(byte)


def objectify(routine, filename):
    file = open(filename, "wb")
    # write version number 1.0, 2 bytes
    file.write(hexit(1, 1))
    file.write(hexit(0, 1))
    # write number of data values, 1 byte
    no_data = len(routine["data"])
    file.write(hexit(no_data, 1))
    # write data as 4 byte ints
    for data in routine["data"]:
        file.write(hexit(data, 4))
    # write number of instructions, 1 byte
    no_ins = len(routine["ins"])
    file.write(hexit(no_ins, 1))
    # write instructions, 1 byte each
    for ins in routine["ins"]:
        file.write(hexit(ins, 1))
    file.close()


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    if len(args) == 2:
        routine = asm(args[0])
        objectify(routine, args[1])
    else:
        print("Usage: asm.py input.imp output.obj")
